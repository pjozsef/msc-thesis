package com.github.pjozsef.thesis.dsp

import com.beust.jcommander.JCommander
import com.beust.jcommander.ParameterException
import com.github.pjozsef.thesis.dsp.cli.*
import com.github.pjozsef.thesis.dsp.utils.*
import java.awt.image.BufferedImage
import java.io.File
import java.nio.file.Files
import java.nio.file.Paths
import kotlin.system.measureTimeMillis

fun main(args: Array<String>) {
    val id3Command = TagCommand()
    val wavCommand = WavCommand()
    val spectrogramCommand = SpectrogramCommand()
    val sectionCommand = SectionCommand()
    val listCommand = ListCommand()
    val exportCommand = ExportCommand()
    val exportListCommand = ExportListCommand()
    val jcommander = JCommander.newBuilder()
            .addCommand(Command.TAG, id3Command)
            .addCommand(Command.WAV, wavCommand)
            .addCommand(Command.SPECTROGRAM, spectrogramCommand)
            .addCommand(Command.SECTION, sectionCommand)
            .addCommand(Command.LIST, listCommand)
            .addCommand(Command.EXPORT, exportCommand)
            .addCommand(Command.EXPORT_LIST, exportListCommand)
            .build()

    try {
        jcommander.parse(*args)
        when (jcommander.parsedCommand) {
            Command.TAG -> listId3Tags(id3Command)
            Command.WAV -> convertWav(wavCommand)
            Command.SPECTROGRAM -> createSpectrogram(spectrogramCommand)
            Command.SECTION -> createSection(sectionCommand)
            Command.LIST -> createMp3List(listCommand)
            Command.EXPORT -> exportData(exportCommand)
            Command.EXPORT_LIST -> exportList(exportListCommand)
            else -> jcommander.usage()
        }
    } catch (pe: ParameterException) {
        println(pe.message)
        pe.usage()
    }
    System.exit(0)
}

private fun listId3Tags(tagCommand: TagCommand) {
    val print: (Any) -> Unit = { println(it) }
    getId3Tag(tagCommand.files.first()).fold(print, print)
}

private fun convertWav(wavCommand: WavCommand) {
    convertToWav(wavCommand.files.first())
}

private fun createSpectrogram(spectrogramCommand: SpectrogramCommand) {
    val wavPath = spectrogramCommand.files.first()
    val magnitudes = fftMagnitudesFrom(wavPath, spectrogramCommand.chunkSize, spectrogramCommand.height)

    val spectrogram = time("creating spectrogram") {
        val binSize = spectrogramCommand.chunkSize / 2
        spectrogramImage(magnitudes, spectrogramCommand.colored, binSize, spectrogramCommand.markerLines)
    }

    println("width: ${spectrogram.width}")
    println("height: ${spectrogram.height}")

    val outputPath = outputPath(wavPath)

    saveImageMeasured(spectrogram, outputPath)
}

private fun createSection(sectionCommand: SectionCommand) {
    sectionCommand.validate()

    export(sectionCommand.files.first(),
            sectionCommand.chunkSize,
            sectionCommand.height,
            sectionCommand.windowSize,
            sectionCommand.stepSize,
            sectionCommand.percentiles,
            sectionCommand.output,
            sectionCommand.export)
}

private fun exportList(exportListCommand: ExportListCommand) {
    time("complete operation") {
        val finishedTracks = exportListCommand
                .currentProgress
                .readText()
                .split(Regex("\\n"))

        exportListCommand.files
                .asSequence()
                .flatMap {
                    File(it).readText()
                            .split(Regex("\\n"))
                            .asSequence()
                }
                .filter {
                    !finishedTracks.contains(it)
                }
                .forEach {
                    val customPercentiles = (15..100 step 5).toList()
                    val exportCommand = ExportCommand(customPercentiles).apply {
                        files = listOf(it)
                        outputDirectory = exportListCommand.outputDirectory
                    }
                    exportData(exportCommand)

                    exportListCommand.currentProgress.appendOrCreate(it)
                }
    }
}

private fun exportData(exportCommand: ExportCommand) {
    val inputFile = exportCommand.files.first()

    val isMp3 = exportCommand.files.first().endsWith(".mp3")

    val fileName = if (isMp3) {
        time("converting to wav") {
            convertToWav(inputFile)
            inputFile.replace(".mp3", ".wav")
        }
    } else {
        inputFile
    }

    export(fileName,
            exportCommand.chunkSize,
            exportCommand.height,
            exportCommand.windowSize,
            exportCommand.stepSize,
            exportCommand.percentiles,
            exportCommand.output,
            exportCommand.export,
            exportCommand.outputDirectory,
            true)

    if (isMp3) {
        time("deleting temporary wav file") {
            Files.delete(Paths.get(fileName))
        }
    }
}

private fun export(
        wavPath: String,
        chunkSize: Int,
        height: Int?,
        windowSize: Int,
        stepSize: Int,
        percentiles: List<Int>,
        output: Boolean,
        export: Boolean,
        outputDirectory: File? = null,
        fileNameFromTags: Boolean = false
) {
    val magnitudes = fftMagnitudesFrom(wavPath, chunkSize, height)

    val sections = time("find sections") {
        findSections(magnitudes, windowSize, stepSize, percentiles)
    }

    percentiles.zip(sections).forEach { (percentile, section) ->
        val (start, end) = section.asTimeInterval(chunkSize)
        if (output) {
            println("${percentile}th percentile -> [${start.toPrettyString()}..${end.toPrettyString()}]")
        }
        if (export) {
            val fileName = outputPath(wavPath, outputDirectory, postfix = "__$percentile", fileNameFromTags = fileNameFromTags)
            println(fileName)
            saveImageMeasured(section.asImage(magnitudes).asBlackAndWhite(), fileName)
        }
    }
}

private fun createMp3List(listCommand: ListCommand) {
    fun StringBuilder.appendIfNeeded(needed: Boolean, selector: () -> String) {
        if (needed) {
            append(selector())
        }
    }

    listCommand.validate()
    listCommand.folders.asSequence().flatMap {
        recursivelyFind(it, ".*\\.mp3")
    }.map {
        getId3Tag(it.absolutePath)
    }.forEach { id3TagDisjunction ->

        id3TagDisjunction.fold({ problem ->
            val message = "Problem with mp3: $problem"
            if (!listCommand.ignoreErrors) {
                throw IllegalArgumentException(message)
            } else {
                System.err.println("${id3TagDisjunction.component1()}")
            }
        }, { id3Tag ->
            val output = buildString {
                appendIfNeeded(listCommand.listPath) { id3Tag.file }
                appendIfNeeded(listCommand.listArtist) { id3Tag.artist }
                appendIfNeeded(listCommand.listAlbum) { id3Tag.album }
                appendIfNeeded(listCommand.listSong) { id3Tag.title }
            }
            println(output)
        })
    }
}

private fun fftMagnitudesFrom(wavPath: String, chunkSize: Int, cropHeight: Int? = null): List<DoubleArray> {
    println(wavPath)
    val data = wavArray(wavPath)
    //8820
    //8192 2^13
    val fft = time("calculating fft") {
        fft(data, chunkSize)
    }
    val magnitudes = time("calculating magnitude") {
        magnitude(fft, cropHeight)
    }

    return magnitudes
}

private fun outputPath(
        inputPath: String,
        outputDirectory: File? = null,
        prefix: String = "",
        postfix: String = "",
        fileNameFromTags: Boolean = false): String {
    return inputPath.let {
        val file = File(it).absoluteFile
        val directory = outputDirectory ?: file.parent
        val sep = File.separator

        val fileName = if (fileNameFromTags) {
            val mp3Path = inputPath.replace(".wav", ".mp3")
            getId3Tag(mp3Path).fold(
                    { problem -> throw IllegalArgumentException(problem.toString()) },
                    { tag -> "${tag.artist}__${tag.album}__${tag.title}" })
        } else file.nameWithoutExtension

        val extension = ".png"
        "$directory$sep$prefix$fileName$postfix$extension"
    }
}

private fun saveImageMeasured(image: BufferedImage, outputPath: String) {
    time("image save") {
        saveImage(image, outputPath)
    }
}

private fun <T> time(label: String, action: () -> T): T {
    var t: T? = null
    val time = measureTimeMillis {
        t = action()
    }
    println("$label took ${time / 1000.0} seconds")
    return t!!
}

package com.github.pjozsef.thesis.dsp

import com.beust.jcommander.JCommander
import com.beust.jcommander.ParameterException
import com.github.pjozsef.thesis.dsp.cli.*
import com.github.pjozsef.thesis.dsp.utils.*
import java.io.File
import kotlin.system.measureTimeMillis

fun main(args: Array<String>) {
    val id3Command = TagCommand()
    val wavCommand = WavCommand()
    val spectrogramCommand = SpectrogramCommand()
    val sectionCommand = SectionCommand()
    val listCommand = ListCommand()
    val jcommander = JCommander.newBuilder()
            .addCommand(Command.TAG, id3Command)
            .addCommand(Command.WAV, wavCommand)
            .addCommand(Command.SPECTROGRAM, spectrogramCommand)
            .addCommand(Command.SECTION, sectionCommand)
            .addCommand(Command.LIST, listCommand)
            .build()

    try {
        jcommander.parse(*args)
        when (jcommander.parsedCommand) {
            Command.TAG -> listId3Tags(id3Command)
            Command.WAV -> convertWav(wavCommand)
            Command.SPECTROGRAM -> createSpectrogram(spectrogramCommand)
            Command.SECTION -> createSection(sectionCommand)
            Command.LIST -> createMp3List(listCommand)
            else -> jcommander.usage()
        }
    } catch (pe: ParameterException) {
        println(pe.message)
        pe.usage()
    }
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

    val outputPath = wavPath.let {
        val file = File(it).absoluteFile
        val directory = file.parent
        val sep = File.separator
        val fileName = file.nameWithoutExtension
        val extension = ".png"
        "$directory$sep$fileName$extension"
    }

    time("image save") {
        saveImage(spectrogram, outputPath)
    }

    System.exit(0)
}

private fun createSection(sectionCommand: SectionCommand) {
    val wavPath = sectionCommand.files.first()
    val magnitudes = fftMagnitudesFrom(wavPath, sectionCommand.chunkSize)

    val sections = time("find sections") {
        findSections(magnitudes, sectionCommand.windowSize, sectionCommand.stepSize, sectionCommand.percentiles)
    }

    sectionCommand.percentiles.zip(sections).forEach {
        val percentile = it.first
        val (start, end) = it.second.asTimeInterval(sectionCommand.chunkSize)
        println("${percentile}th percentile -> [${start.toPrettyString()}..${end.toPrettyString()}]")
    }
}

private fun createMp3List(listCommand: ListCommand) {
    fun StringBuilder.appendIfNeeded(needed: Boolean, selector: () -> String) {
        if (needed) {
            append(selector())
        }
    }

    listCommand.validate()
    listCommand.folders.flatMap {
        recursivelyFind(it, ".*\\.mp3")
    }.map {
        getId3Tag(it.absolutePath)
    }.forEach { id3TagDisjunction ->
        val id3TagOrNot = id3TagDisjunction.fold({
            if (listCommand.ignoreErrors) null else throw IllegalArgumentException("Problem with mp3: $it")
        }, {
            it
        })
        id3TagOrNot?.let { id3Tag ->
            val output = buildString {
                appendIfNeeded(listCommand.listPath) { id3Tag.file }
                appendIfNeeded(listCommand.listArtist) { id3Tag.artist }
                appendIfNeeded(listCommand.listAlbum) { id3Tag.album }
                appendIfNeeded(listCommand.listSong) { id3Tag.title }
            }
            println(output)
        }
    }
}

private fun fftMagnitudesFrom(wavPath: String, chunkSize: Int, cropHeight: Int? = null): List<DoubleArray> {
    val data = wavArray(wavPath)
    //8820
    //8192 2^13
    val fft = time("calculating fft") {
        fft(data, chunkSize)
    }
    val magnitudes = time("converting magnitude") {
        magnitude(fft, cropHeight)
    }

    return magnitudes
}

private fun <T> time(label: String, action: () -> T): T {
    var t: T? = null
    val time = measureTimeMillis {
        t = action()
    }
    println("$label took ${time / 1000.0} seconds")
    return t!!
}

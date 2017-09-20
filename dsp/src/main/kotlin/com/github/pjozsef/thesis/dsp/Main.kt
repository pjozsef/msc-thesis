package com.github.pjozsef.thesis.dsp

import com.beust.jcommander.JCommander
import com.beust.jcommander.ParameterException
import com.github.pjozsef.thesis.dsp.cli.Command
import com.github.pjozsef.thesis.dsp.cli.SpectrogramCommand
import com.github.pjozsef.thesis.dsp.cli.TagCommand
import com.github.pjozsef.thesis.dsp.cli.WavCommand
import com.github.pjozsef.thesis.dsp.utils.*
import java.io.File
import kotlin.system.measureTimeMillis

fun main(args: Array<String>) {
    val id3Command = TagCommand()
    val wavCommand = WavCommand()
    val spectrogramCommand = SpectrogramCommand()
    val jcommander = JCommander.newBuilder()
            .addCommand(Command.TAG, id3Command)
            .addCommand(Command.WAV, wavCommand)
            .addCommand(Command.SPECTROGRAM, spectrogramCommand)
            .build()

    try {
        jcommander.parse(*args)
        when (jcommander.parsedCommand) {
            Command.TAG -> listId3Tags(id3Command)
            Command.WAV -> convertWav(wavCommand)
            Command.SPECTROGRAM -> createSpectrogram(spectrogramCommand)
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
    val data = wavArray(wavPath)
    //8820
    //8192 2^13
    val fft = time("calculating fft") {
        fft(data, spectrogramCommand.chunkSize)
    }
    val magnitudes = time("converting magnitude") {
        magnitude(fft)
    }
    val spectrogram = time("creating spectrogram") {
        spectrogramImage(magnitudes)
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

    time("image save"){
        saveImage(spectrogram, outputPath)
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
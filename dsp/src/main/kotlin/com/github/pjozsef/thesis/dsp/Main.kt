package com.github.pjozsef.thesis.dsp

import com.beust.jcommander.JCommander
import com.beust.jcommander.ParameterException
import com.github.pjozsef.thesis.dsp.cli.Command
import com.github.pjozsef.thesis.dsp.cli.TagCommand
import com.github.pjozsef.thesis.dsp.cli.WavCommand
import com.github.pjozsef.thesis.dsp.utils.*

fun main(args: Array<String>) {
    val id3Command = TagCommand()
    val wavCommand = WavCommand()
    val jcommander = JCommander.newBuilder()
            .addCommand(Command.TAG, id3Command)
            .addCommand(Command.WAV, wavCommand)
            .build()

    try {
        jcommander.parse(*args)
        when (jcommander.parsedCommand) {
            Command.TAG -> listId3Tags(id3Command)
            Command.WAV -> convertWav(wavCommand)
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
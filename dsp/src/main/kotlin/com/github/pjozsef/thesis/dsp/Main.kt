package com.github.pjozsef.thesis.dsp

import com.beust.jcommander.JCommander
import com.beust.jcommander.ParameterException
import com.github.pjozsef.thesis.dsp.cli.Command
import com.github.pjozsef.thesis.dsp.cli.Id3Command
import com.github.pjozsef.thesis.dsp.utils.getId3Tag

fun main(args: Array<String>) {
    val id3Command = Id3Command()
    val jcommander = JCommander.newBuilder()
            .addCommand(Command.ID3, id3Command)
            .build()

    try {
        jcommander.parse(*args)
        when (jcommander.parsedCommand) {
            Command.ID3 -> listId3Tags(id3Command)
            else -> jcommander.usage()
        }
    } catch (pe: ParameterException) {
        println(pe.message)
        pe.usage()
    }
}

private fun listId3Tags(id3Command: Id3Command){
    val print: (Any)->Unit = {println(it)}
    getId3Tag(id3Command.files.first()).fold(print, print)
}
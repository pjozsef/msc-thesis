package com.github.pjozsef.thesis.data

import com.beust.jcommander.JCommander
import com.beust.jcommander.ParameterException
import com.github.pjozsef.thesis.data.cli.Command
import com.github.pjozsef.thesis.data.cli.CsvCommand
import org.tensorflow.SavedModelBundle

fun main(args: Array<String>) {
    val csvCommand = CsvCommand()
    val jcommander = JCommander.newBuilder()
            .addCommand(Command.ENCODE_CSV, csvCommand)
            .build()

    try {
        jcommander.parse(*args)
        when (jcommander.parsedCommand) {
            Command.ENCODE_CSV -> exportToCsv(csvCommand)
            else -> jcommander.usage()
        }
    } catch (pe: ParameterException) {
        println(pe.message)
        pe.usage()
    }
    System.exit(0)
}

fun exportToCsv(csvCommand: CsvCommand) {
    val model = SavedModelBundle.load(csvCommand.model, "serve")
    println(model.graph().operations())
}

package com.github.pjozsef.thesis.data.cli

import com.beust.jcommander.Parameter
import com.beust.jcommander.Parameters

sealed class Command {
    companion object {
        const val ENCODE_CSV = "encodecsv"
    }
}

@Parameters(commandDescription = "Encode images with the autoencoder into csv file")
class CsvCommand : Command() {
    @Parameter(required = true, description = "<folder containing image files (800,20)>")
    lateinit var files: List<String>

    @Parameter(names = ["-m", "--model"], required = true, description = "Path to the encoder model to use")
    lateinit var model: String

    @Parameter(names = ["-p", "--percentile"], required = true, description = "Path to the encoder model to use")
    var percentile: Int = -1

    @Parameter(names = ["-o", "--output"], description = "Output folder for csv")
    var output: String = "encodings.csv"

    @Parameter(names = ["-a", "--append"], description = "Append to csv if it already exists")
    var append: Boolean = false
}

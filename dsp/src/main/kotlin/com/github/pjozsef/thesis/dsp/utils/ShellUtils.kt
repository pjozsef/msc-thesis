package com.github.pjozsef.thesis.dsp.utils

import java.io.InputStream
import java.util.concurrent.TimeUnit


data class CommandLineOutput(val exitValue: Int,
                             val sout: InputStream,
                             val serr: InputStream)

fun execute(vararg commands: String): CommandLineOutput {
    val processBuilder = ProcessBuilder(*commands)

    val process = processBuilder.start()

    val sout = process.inputStream
    val serr = process.errorStream

    process.waitFor(10, TimeUnit.MINUTES)

    val exitValue = process.exitValue()

    return CommandLineOutput(exitValue, sout, serr)
}
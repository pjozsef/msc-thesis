package com.github.pjozsef.thesis.dsp.utils

import java.io.File

fun recursivelyFind(folderPath: String, regexString: String): List<File> {

    fun rec(file: File, regex: Regex, accumulated: MutableList<File>): List<File> = when {
        file.isDirectory -> {
            val (files, folders) = file.listFiles().partition { it.isFile }
            (files + folders).forEach { child ->
                rec(child, regex, accumulated)
            }
            accumulated
        }
        file.isFile -> {
            if (regex.matches(file.absolutePath)) {
                accumulated += file
            }
            accumulated
        }
        else -> accumulated
    }

    val folder = File(folderPath)
    require(folder.exists(), { "The given path must exist!" })
    require(folder.isDirectory, { "The given path must be a folder!" })
    return rec(folder, Regex(regexString), mutableListOf())
}
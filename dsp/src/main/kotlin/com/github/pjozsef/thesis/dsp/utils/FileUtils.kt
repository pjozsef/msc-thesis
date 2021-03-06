package com.github.pjozsef.thesis.dsp.utils

import java.io.File

fun recursivelyFind(folderPath: String, regexString: String): Sequence<File> {
    val regex = Regex(regexString)
    val folder = File(folderPath)

    require(folder.exists(), { "The given path must exist!" })
    require(folder.isDirectory, { "The given path must be a folder!" })

    return folder.walk().filter { regex.matches(it.absolutePath) }
}

fun File.appendOrCreate(content: String) {
    if (!this.exists()) {
        this.parentFile.mkdirs()
        this.createNewFile()
        this.writeText(content)
    } else {
        this.appendText("\n$content")
    }
}
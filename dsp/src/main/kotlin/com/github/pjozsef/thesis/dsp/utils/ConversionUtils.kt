package com.github.pjozsef.thesis.dsp.utils

import java.io.File

fun convertToWav(path: String) {
    val file = File(path).absoluteFile
    val fileName = file.nameWithoutExtension
    val folder = file.parent
    val sep = File.separator
    val outputPath = "$folder$sep$fileName.wav"
    execute("ffmpeg",
            "-i", file.absolutePath,
            "-ac", "1",
            "-ar", "44100",
            "-filter:a", "loudnorm",
            "-y",
            outputPath)
}
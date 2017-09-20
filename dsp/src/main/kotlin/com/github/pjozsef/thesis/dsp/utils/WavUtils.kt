package com.github.pjozsef.thesis.dsp.utils

import java.io.File
import javax.sound.sampled.AudioSystem

fun wavArray(path: String): DoubleArray {
    val wav = AudioSystem.getAudioInputStream(File(path))
    val format = wav.format

    require(!format.isBigEndian)
    require(format.channels == 1)
    require(format.sampleRate == 44100f)
    require(format.sampleSizeInBits == 16)

    val rawBytes = wav.readBytes()
    require(rawBytes.size % 2 == 0)

    val values = DoubleArray(rawBytes.size/2)
    for(i in 0..rawBytes.lastIndex step 2){
        val smallByte = rawBytes[i]
        val largeByte = rawBytes[i+1]
        val value = largeByte.toInt().shl(8) + smallByte
        values[i/2] = value.toDouble()
    }

    return values
}
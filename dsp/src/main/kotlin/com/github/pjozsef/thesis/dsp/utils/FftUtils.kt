package com.github.pjozsef.thesis.dsp.utils

import org.jtransforms.fft.DoubleFFT_1D
import java.util.*

fun fft(array: DoubleArray, chunkSize: Int): List<DoubleArray> {
    val resultSize = array.size / chunkSize
    val result = ArrayList<DoubleArray>(resultSize)
    for (i in 0 until resultSize) {
        val start = chunkSize * i
        val end = start + chunkSize - 1
        val input = array.sliceArray(start..end)
        result += fft(input)
    }
    return result
}

fun fft(array: DoubleArray): DoubleArray {
    val result = Arrays.copyOf(array, array.size)
    val fft = DoubleFFT_1D(result.size.toLong())
    fft.realForward(result)
    return result
}

fun magnitude(arrays: List<DoubleArray>) = arrays.map { magnitude(it) }

fun magnitude(array: DoubleArray): DoubleArray {
    val result = DoubleArray(array.size / 2)
    for (i in 0 until array.size step 2) {
        val re = array[i]
        val im = array[i + 1]
        result[i / 2] = Math.sqrt(re * re + im * im)
    }
    return result
}
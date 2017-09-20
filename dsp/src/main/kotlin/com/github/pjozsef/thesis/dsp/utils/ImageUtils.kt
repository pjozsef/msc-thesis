package com.github.pjozsef.thesis.dsp.utils

import java.awt.Color
import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

fun spectrogramImage(magnitudes: List<DoubleArray>): BufferedImage {
    val result = BufferedImage(magnitudes.size, magnitudes[0].size, BufferedImage.TYPE_INT_RGB)
    val max = magnitudes.map { it.max() ?: 0.0 }.max() ?: 0.0
    require(max > 0.0)

    for (row in magnitudes.indices) {
        val height = magnitudes[row].size - 1
        for (column in magnitudes[row].indices) {
            val color = Color.getHSBColor(
                    0.0f,
                    0.0f,
                    (magnitudes[row][height - column] / max).toFloat() * 5).rgb
            result.setRGB(row, column, color)
        }
    }
    return result
}

fun saveImage(image: BufferedImage, path: String) {
    val outputFile = File(path)
    ImageIO.write(image, "png", outputFile)
}
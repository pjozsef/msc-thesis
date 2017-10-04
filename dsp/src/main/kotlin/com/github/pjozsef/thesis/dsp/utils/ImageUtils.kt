package com.github.pjozsef.thesis.dsp.utils

import java.awt.Color
import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

fun spectrogramImage(magnitudes: List<DoubleArray>, colored: Boolean): BufferedImage {
    val result = BufferedImage(magnitudes.size, magnitudes[0].size, BufferedImage.TYPE_INT_RGB)
    val max = magnitudes.map { it.max() ?: 0.0 }.max() ?: 0.0
    require(max > 0.0)

    val hues = if (colored) getHues(magnitudes) else FloatArray(magnitudes.size) { 0.0f }
    val saturation = if (colored) 1.0f else 0.0f

    for (row in magnitudes.indices) {
        val height = magnitudes[row].size - 1
        for (column in magnitudes[row].indices) {
            val color = Color.getHSBColor(
                    hues[row],
                    saturation,
                    (magnitudes[row][height - column] / max).toFloat() * 5).rgb
            result.setRGB(row, column, color)
        }
    }
    return result
}

private fun getHues(input: List<DoubleArray>): FloatArray {
    val size = input.size
    val result = FloatArray(size)
    val percentile25 = percentileToIndex(size, 25)
    val percentile50 = percentileToIndex(size, 50)
    val percentile75 = percentileToIndex(size, 75)
    val percentile100 = percentileToIndex(size, 100)

    val weightedSections = createWeightedSections(input, 1, 1)
    for ((index, weightedSection) in weightedSections.withIndex()) {
        result[weightedSection.second.start] = when (index) {
            in 0..percentile25 -> 0.6f
            in percentile25..percentile50 -> 0.3f
            in percentile50..percentile75 -> 0.17f
            in percentile75..percentile100 -> 0.0f
            else -> error("Invalid index: $index")
        }
    }
    return result
}

fun saveImage(image: BufferedImage, path: String) {
    val outputFile = File(path)
    ImageIO.write(image, "png", outputFile)
}
package com.github.pjozsef.thesis.dsp.utils

import java.awt.Color
import java.awt.image.BufferedImage
import java.io.File
import javax.imageio.ImageIO

fun spectrogramImage(magnitudes: List<DoubleArray>, colored: Boolean, originalBinSize: Int, markerLines: List<Double>): BufferedImage {
    val width = magnitudes.size
    val height = magnitudes[0].size

    val result = imageFromRange(magnitudes, magnitudes.indices, colored)

    markerLines.forEach { frequency ->
        val markerHeight = frequencyToFftBin(frequency, originalBinSize)
        println("marker line frequency ${frequency}Hz mapped to bin $markerHeight")
        for (row in 0 until width) {
            val color = Color.getHSBColor(0f, 1f, 1f).rgb
            result.setRGB(row, height - markerHeight - 1, color)
        }
    }

    return result
}

fun imageFromRange(magnitudes: List<DoubleArray>, range: IntRange, colored: Boolean = false): BufferedImage {
    val height = magnitudes[0].size
    val hues = if (colored) getHues(magnitudes) else FloatArray(magnitudes.size) { 0.0f }
    val saturation = if (colored) 1.0f else 0.0f
    val result = BufferedImage(range.count(), height, BufferedImage.TYPE_INT_RGB)
    val max = magnitudes.map { it.max() ?: 0.0 }.max() ?: 0.0
    require(max > 0.0)

    for (row in range) {
        val rowIndex = row - range.first
        for (column in 0 until height) {
            val color = Color.getHSBColor(
                    hues[row],
                    saturation,
                    (magnitudes[row][height - column - 1] / max).toFloat() * 5).rgb
            result.setRGB(rowIndex, column, color)
        }
    }

    return result
}

fun Section.asImage(magnitudes: List<DoubleArray>): BufferedImage = imageFromRange(magnitudes, start until endExclusive)

fun BufferedImage.asBlackAndWhite(): BufferedImage {
    val bw = BufferedImage(
            this.width,
            this.height,
            BufferedImage.TYPE_BYTE_GRAY)
    val g = bw.createGraphics()
    g.drawImage(this, 0, 0, null)
    g.dispose()
    return bw
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
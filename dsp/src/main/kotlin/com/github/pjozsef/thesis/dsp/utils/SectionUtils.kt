package com.github.pjozsef.thesis.dsp.utils

import java.math.BigDecimal

data class Section(val start: Int, val endExclusive: Int)

fun findSections(input: List<DoubleArray>, windowSize: Int, stepSize: Int, percentiles: List<Int>)
        = findSections(input, windowSize, stepSize, *percentiles.toIntArray())

fun findSections(input: List<DoubleArray>, windowSize: Int, stepSize: Int, vararg percentiles: Int): List<Section> {
    val sections = createWeightedSections(input, windowSize, stepSize)
    val result = ArrayList<Section>()
    for (percentile in percentiles) {
        val index = percentileToIndex(sections.size, percentile)
        result += sections[index].second
    }
    return result
}

fun createWeightedSections(input: List<DoubleArray>, windowSize: Int, stepSize: Int): List<Pair<Double, Section>> {
    val sections = ArrayList<Pair<Double, Section>>()
    for (i in 0..input.size - windowSize step stepSize) {
        val section = Section(i, i + windowSize)
        val sum = input.sumBy(section)
        sections.add(sum to section)
    }

    sections.sortBy { it.first }

    return sections
}

fun percentileToIndex(size: Int, percentile: Int)
        = Math.ceil((size - 1) * percentile / 100.0).toInt()

fun List<DoubleArray>.sumBy(section: Section): Double {
    var sum = 0.0
    for (i in section.start until section.endExclusive) {
        val array = this[i]
        for (j in 0 until array.size) {
            sum += array[j]
        }
    }
    return sum
}

fun Section.asTimeInterval(fftChunkSize: Int) = this.asTimeInterval(fftChunkSize.toBigDecimal())

fun Section.asTimeInterval(fftChunkSize: BigDecimal = 8192.0.bigDecimal()): Pair<BigDecimal, BigDecimal> {
    val baseSampleRate = 44100.0.bigDecimal()
    val samplesPerSecond = baseSampleRate / fftChunkSize
    return this.start.bigDecimal() / samplesPerSecond to this.endExclusive.bigDecimal() / samplesPerSecond
}

fun BigDecimal.toPrettyString(): String {
    val minutes = (this / BigDecimal(60)).setScale(0, BigDecimal.ROUND_DOWN)
    val seconds = (this % BigDecimal(60)).setScale(1, BigDecimal.ROUND_HALF_UP)
    return "${minutes.stripTrailingZeros()}m${seconds.stripTrailingZeros()}s"
}

private fun Number.bigDecimal() = BigDecimal(this.toDouble()).setScale(2, BigDecimal.ROUND_HALF_UP)
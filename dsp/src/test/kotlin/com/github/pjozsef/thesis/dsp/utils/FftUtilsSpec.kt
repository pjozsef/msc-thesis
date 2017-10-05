package com.github.pjozsef.thesis.dsp.utils

import org.amshove.kluent.`should equal`
import org.jetbrains.spek.api.Spek
import org.jetbrains.spek.api.dsl.given
import org.jetbrains.spek.api.dsl.it
import org.jetbrains.spek.api.dsl.on

object FftUtilsSpec : Spek({
    given("Some frequencies") {
        val c1 = 32.70
        val e2 = 82.41
        val a4 = 440.00
        val d6 = 1174.66

        given("a bin size of 512") {
            val binSize = 512

            on("calling frequencyToFftBin") {
                val binC1 = frequencyToFftBin(c1, binSize)
                val binE2 = frequencyToFftBin(e2, binSize)
                val binA4 = frequencyToFftBin(a4, binSize)
                val binD6 = frequencyToFftBin(d6, binSize)

                it("should all be correct") {
                    binC1 `should equal` 0
                    binE2 `should equal` 1
                    binA4 `should equal` 10
                    binD6 `should equal` 27
                }
            }
        }

        given("a bin size of 4048") {
            val binSize = 4048

            on("calling frequencyToFftBin") {
                val binC1 = frequencyToFftBin(c1, binSize)
                val binE2 = frequencyToFftBin(e2, binSize)
                val binA4 = frequencyToFftBin(a4, binSize)
                val binD6 = frequencyToFftBin(d6, binSize)

                it("should all be correct") {
                    binC1 `should equal` 6
                    binE2 `should equal` 15
                    binA4 `should equal` 80
                    binD6 `should equal` 215
                }
            }
        }
    }
})
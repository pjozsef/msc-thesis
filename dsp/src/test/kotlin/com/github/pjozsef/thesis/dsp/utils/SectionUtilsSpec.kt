package com.github.pjozsef.thesis.dsp.utils

import junit.framework.Assert.assertEquals
import org.amshove.kluent.`should equal`
import org.jetbrains.spek.api.Spek
import org.jetbrains.spek.api.dsl.given
import org.jetbrains.spek.api.dsl.it
import org.jetbrains.spek.api.dsl.on
import java.math.BigDecimal

object SectionUtilsSpec : Spek({
    given("a list of DoubleArrays of size 11") {
        lateinit var list: List<DoubleArray>

        beforeEachTest {
            list = listOf(
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 50.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 5.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 1.0, 6.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 10.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 100.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 7.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 19.0),
                    doubleArrayOf(10.0, 10.0, 10.0, -10.0, -10.0, -100.0, 10.0, 10.0, -10.0, 0.0)
            )
        }

        on("calling findSections") {
            val result = findSections(list, 3, 1, 25, 50, 75, 100)

            it("should be correct") {
                result `should equal` listOf(
                        Section(4, 7),
                        Section(2, 5),
                        Section(5, 8),
                        Section(7, 10)
                )
            }
        }

        on("calling sumBy section") {
            val result = list.sumBy(Section(1, 5))

            it("should equal 96") {
                result `should equal` 96.0
            }
        }

        on("getting the 0th percentile index") {
            val index = percentileToIndex(list.size, 0)
            it("the index should be") {
                index `should equal` 0
            }
        }

        on("getting the 100th percentile index") {
            val index = percentileToIndex(list.size, 100)
            it("the index should be") {
                index `should equal` 10
            }
        }

        on("getting the 50th percentile index") {
            val index = percentileToIndex(list.size, 50)
            it("the index should be") {
                index `should equal` 5
            }
        }

        on("getting the 20th percentile index") {
            val index = percentileToIndex(list.size, 20)
            it("the index should be") {
                index `should equal` 2
            }
        }
    }

    given("a list of DoubleArrays of size 6") {
        lateinit var list: List<DoubleArray>

        beforeEachTest {
            list = listOf(
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 3.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 50.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 2.0, 1.0, 1.0, 1.0, 1.0, 1.0),
                    doubleArrayOf(1.0, 1.0, 1.0, 1.0, 1.0, 3.0, 1.0, 1.0, 1.0, 1.0)
            )
        }

        on("calling findSections") {
            val result = findSections(list, 2, 2, 0, 30, 60, 90, 100)

            it("should be correct") {
                result `should equal` listOf(
                        Section(0, 2),
                        Section(4, 6),
                        Section(2, 4),
                        Section(2, 4),
                        Section(2, 4)
                )
            }
        }

        on("getting the 20th percentile index") {
            val index = percentileToIndex(list.size, 20)
            it("the index should be") {
                index `should equal` 1
            }
        }

        on("getting the 75th percentile index") {
            val index = percentileToIndex(list.size, 75)
            it("the index should be") {
                index `should equal` 4
            }
        }

    }

    given("some sections") {
        val section1 = Section(0, 6)
        val section2 = Section(5, 9)
        val section3 = Section(60, 800)
        val section4 = Section(1500, 2320)

        on("calling getSecond on them") {
            val interval1 = section1.asTimeInterval()
            val interval2 = section2.asTimeInterval()
            val interval3 = section3.asTimeInterval()
            val interval4 = section4.asTimeInterval()

            it("should all be correct") {
                interval1.first.toString() `should equal` "0.00"
                interval1.second.toString() `should equal` "1.12"

                interval2.first.toString() `should equal` "0.93"
                interval2.second.toString() `should equal` "1.67"

                interval3.first.toString() `should equal` "11.15"
                interval3.second.toString() `should equal` "148.70"

                interval4.first.toString() `should equal` "278.81"
                interval4.second.toString() `should equal` "431.23"
            }
        }
    }

    given("some BigDecimals") {
        val d1 = BigDecimal("60.0")
        val d2 = BigDecimal("35.0")
        val d3 = BigDecimal("65.3")
        val d4 = BigDecimal("125.5")
        val d5 = BigDecimal("60.68")
        val d6 = BigDecimal("60.644444")

        on("calling prettyToString on them") {
            val s1 = d1.toPrettyString()
            val s2 = d2.toPrettyString()
            val s3 = d3.toPrettyString()
            val s4 = d4.toPrettyString()
            val s5 = d5.toPrettyString()
            val s6 = d6.toPrettyString()

            it("should all be correct") {
                s1 `should equal` "1m0s"
                s2 `should equal` "0m35s"
                s3 `should equal` "1m5.3s"
                s4 `should equal` "2m5.5s"
                s5 `should equal` "1m0.7s"
                s6 `should equal` "1m0.6s"
            }
        }
    }
})

data class DoubleAssertion(val result: Double, val expected: Double)

infix fun Double.shouldBeAround(theOther: Double) = DoubleAssertion(this, theOther)
infix fun Double.shouldBeCloseTo(theOther: Double) = DoubleAssertion(this, theOther)
infix fun DoubleAssertion.withDelta(delta: Double) = assertEquals(this.expected, this.result, delta)

data class FloatAssertion(val result: Float, val expected: Float)

infix fun Float.shouldBeAround(theOther: Float) = FloatAssertion(this, theOther)
infix fun FloatAssertion.withDelta(delta: Float) = assertEquals(this.expected, this.result, delta)
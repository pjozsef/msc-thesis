package com.github.pjozsef.thesis.dsp.utils

import org.amshove.kluent.`should equal`
import org.amshove.kluent.shouldThrow
import org.jetbrains.spek.api.Spek
import org.jetbrains.spek.api.dsl.given
import org.jetbrains.spek.api.dsl.it
import org.jetbrains.spek.api.dsl.on
import java.io.File

object FileUtilsSpec : Spek({
    given("an not existing folder") {
        val folder = "/asdf"

        on("supplying a missing folder to recursivelyFind") {
            val call = { recursivelyFind(folder, ".*\\.txt") }

            it("should throw an exception") {
                call shouldThrow IllegalArgumentException::class
            }
        }
    }

    given("a file") {
        val file = this.javaClass.getResource("/com/github/pjozsef/thesis/dsp/utils/no_tags.mp3").path

        on("supplying a file to recursivelyFind") {
            val call = { recursivelyFind(file, ".*\\.txt") }

            it("should throw an exception") {
                call shouldThrow IllegalArgumentException::class
            }
        }
    }
    given("a folder with nested mp3 files") {
        val folder = this.javaClass.getResource("/com/github/pjozsef/thesis/dsp/utils/nestedFolder").path

        on("calling recursivelyFind with .mp3 pattern") {
            val files = recursivelyFind(folder, ".*\\.mp3").toList().sorted()

            it("should list all the mp3 files in the folder") {
                val folder = File(this.javaClass.getResource("/com/github/pjozsef/thesis/dsp/utils/nestedFolder").file)
                files `should equal` listOf(
                        File(folder, "/01.mp3"),
                        File(folder, "/02.mp3"),
                        File(folder, "/03.mp3"),
                        File(folder, "/deeplyNested/04.mp3")
                ).sorted()
            }
        }
    }
})
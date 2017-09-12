package com.github.pjozsef.thesis.dsp.utils

import com.github.pjozsef.thesis.dsp.exception.MissingFileProblem
import com.github.pjozsef.thesis.dsp.exception.MissingTagsProblem
import com.github.pjozsef.thesis.dsp.exception.NotMp3FileProblem
import org.amshove.kluent.`should equal`
import org.jetbrains.spek.api.Spek
import org.jetbrains.spek.api.dsl.given
import org.jetbrains.spek.api.dsl.it
import org.jetbrains.spek.api.dsl.on
import org.junit.Assert

object Id3UtilsSpec : Spek({
    fun file(name: String) = this.javaClass
            .getResource("/com/github/pjozsef/thesis/dsp/utils/$name")
            .path

    given("A missing file") {
        val filePath = "invalid.mp3"

        on("calling getId3Tag") {
            val result = getId3Tag(filePath)

            it("should return a MissingFileProblem") {
                result.fold({ problem ->
                    when (problem) {
                        is MissingFileProblem -> problem.file `should equal` filePath
                        else -> Assert.fail("Must be a MissingFileProblem, but was $problem")
                    }
                }, { tag -> Assert.fail("Must be a problem, but was $tag!") })
            }
        }
    }

    given("A file that is not mp3") {
        val filePath = file("not_mp3.txt")

        on("calling getId3Tag") {
            val result = getId3Tag(filePath)

            it("should return a NotMp3FileProblem") {
                result.fold({ problem ->
                    when (problem) {
                        is NotMp3FileProblem -> problem.file `should equal` filePath
                        else -> Assert.fail("Must be a NotMp3FileProblem, but was $problem")
                    }
                }, { tag -> Assert.fail("Must be a problem, but was $tag!") })
            }
        }
    }

    given("An mp3 file with no Id3Tags") {
        val filePath = file("no_tags.mp3")

        on("calling getId3Tag") {
            val result = getId3Tag(filePath)

            it("should return a MissingTagsProblem") {
                result.fold({ problem ->
                    when (problem) {
                        is MissingTagsProblem -> {
                            problem.file `should equal` filePath
                            problem.missingTags `should equal` Id3Tag.Type.values().toList()
                        }
                        else -> Assert.fail("Must be a MissingTagsProblem, but was $problem")
                    }
                }, { tag -> Assert.fail("Must be a problem, but was $tag!") })
            }
        }
    }

    given("An mp3 file with some, but not all mandatory Id3Tags") {
        val filePath = file("some_tags.mp3")

        on("calling getId3Tag") {
            val result = getId3Tag(filePath)

            it("should return a MissingTagsProblem") {
                result.fold({ problem ->
                    when (problem) {
                        is MissingTagsProblem -> {
                            problem.file `should equal` filePath
                            problem.missingTags `should equal` listOf(Id3Tag.Type.ARTIST, Id3Tag.Type.ALBUM)
                        }
                        else -> Assert.fail("Must be a MissingTagsProblem, but was $problem")
                    }
                }, { tag -> Assert.fail("Must be a problem, but was $tag!") })
            }
        }
    }

    given("An mp3 file with all mandatory Id3Tags") {
        val filePath = file("tags.mp3")

        on("calling getId3Tag") {
            val result = getId3Tag(filePath)

            it("should return a MissingTagsProblem") {
                result.fold({ problem ->
                    Assert.fail("Must be an Id3Tag, but was $problem!")
                }, { tag ->
                    tag.artist `should equal` "artist_name"
                    tag.title `should equal` "title_name"
                    tag.album `should equal` "album_name"
                    tag.file `should equal` filePath
                })
            }
        }
    }


})
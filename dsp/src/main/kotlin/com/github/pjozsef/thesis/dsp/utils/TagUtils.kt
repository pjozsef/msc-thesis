package com.github.pjozsef.thesis.dsp.utils


import com.github.pjozsef.thesis.dsp.exception.MissingFileProblem
import com.github.pjozsef.thesis.dsp.exception.MissingTagsProblem
import com.github.pjozsef.thesis.dsp.exception.NotMp3FileProblem
import com.github.pjozsef.thesis.dsp.exception.Problem
import com.mpatric.mp3agic.Mp3File
import org.funktionale.either.Disjunction
import org.funktionale.validation.Validation
import java.io.File

data class Id3Tag(val artist: String, val title: String, val album: String, val file: String) {
    enum class Type { ARTIST, TITLE, ALBUM }
}

fun getId3Tag(filePath: String): Disjunction<Problem, Id3Tag> = when {
    !File(filePath).exists() -> Disjunction.left(MissingFileProblem(filePath))
    !filePath.endsWith("mp3") -> Disjunction.left(NotMp3FileProblem(filePath))
    else -> extractTag(filePath)
}

private fun extractTag(filePath: String): Disjunction<Problem, Id3Tag> {
    fun String?.asDisjunction(type: Id3Tag.Type) = if (this == null || this.isBlank()) Disjunction.left(type) else Disjunction.right(this)
    val mp3 = Mp3File(filePath)

    val artist = (mp3.id3v2Tag?.artist ?: mp3.id3v1Tag?.artist).asDisjunction(Id3Tag.Type.ARTIST)
    val title = (mp3.id3v2Tag?.title ?: mp3.id3v1Tag?.title).asDisjunction(Id3Tag.Type.TITLE)
    val album = (mp3.id3v2Tag?.album ?: mp3.id3v1Tag?.album).asDisjunction(Id3Tag.Type.ALBUM)

    val tags = arrayOf(artist, title, album)
    val validation = Validation(*tags)

    return if (validation.hasFailures) {
        Disjunction.left(MissingTagsProblem(filePath, validation.failures))
    } else {
        Disjunction.right(Id3Tag(
                artist.get(),
                title.get(),
                album.get(),
                filePath
        ))
    }
}
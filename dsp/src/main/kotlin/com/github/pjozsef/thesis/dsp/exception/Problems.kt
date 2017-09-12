package com.github.pjozsef.thesis.dsp.exception

import com.github.pjozsef.thesis.dsp.utils.Id3Tag

sealed class Problem

data class MissingFileProblem(val file: String): Problem()
data class NotMp3FileProblem(val file: String): Problem()
data class MissingTagsProblem(val file: String, val missingTags: List<Id3Tag.Type>): Problem()


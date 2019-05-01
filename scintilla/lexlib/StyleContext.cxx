// Scintilla source code edit control
/** @file StyleContext.cxx
 ** Lexer infrastructure.
 **/
// Copyright 1998-2004 by Neil Hodgson <neilh@scintilla.org>
// This file is in the public domain.

#include <cstdlib>
#include <cassert>

#include "ILexer.h"

#include "LexAccessor.h"
#include "Accessor.h"
#include "StyleContext.h"
#include "CharacterSet.h"

using namespace Scintilla;

bool StyleContext::MatchIgnoreCase(const char *s) const noexcept {
	if (MakeLowerCase(ch) != static_cast<unsigned char>(*s)) {
		return false;
	}
	s++;
	if (MakeLowerCase(chNext) != static_cast<unsigned char>(*s)) {
		return false;
	}
	s++;
	for (int n = 2; *s; n++) {
		if (*s != MakeLowerCase(styler.SafeGetCharAt(currentPos + n))) {
			return false;
		}
		s++;
	}
	return true;
}

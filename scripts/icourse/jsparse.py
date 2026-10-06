"""Minimal parser for JS object literals embedded in HTML (unquoted keys, // and /* */ comments)."""

class JSParse:
    def __init__(self, s, i=0):
        self.s = s
        self.i = i
        self.n = len(s)

    def skip_ws(self):
        while self.i < self.n:
            c = self.s[self.i]
            if c in ' \t\r\n':
                self.i += 1
            elif c == '/' and self.i + 1 < self.n and self.s[self.i+1] == '/':
                j = self.s.find('\n', self.i)
                self.i = self.n if j < 0 else j
            elif c == '/' and self.i + 1 < self.n and self.s[self.i+1] == '*':
                j = self.s.find('*/', self.i + 2)
                self.i = self.n if j < 0 else j + 2
            else:
                break

    def parse(self):
        self.skip_ws()
        c = self.s[self.i]
        if c == '{':
            return self.parse_obj()
        if c == '[':
            return self.parse_arr()
        if c in '"\'':
            return self.parse_str()
        return self.parse_word()

    def parse_obj(self):
        self.i += 1  # {
        obj = {}
        while True:
            self.skip_ws()
            if self.s[self.i] == '}':
                self.i += 1
                return obj
            if self.s[self.i] in '"\'':
                key = self.parse_str()
            else:
                key = self.parse_identifier()
            self.skip_ws()
            assert self.s[self.i] == ':', f"expected : at {self.i}: {self.s[self.i-10:self.i+10]!r}"
            self.i += 1
            obj[key] = self.parse()
            self.skip_ws()
            c = self.s[self.i]
            if c == ',':
                self.i += 1
                # allow trailing comma before }
                self.skip_ws()
                if self.s[self.i] == '}':
                    self.i += 1
                    return obj
            elif c == '}':
                self.i += 1
                return obj
            else:
                raise ValueError(f"unexpected char {c!r} at {self.i}")

    def parse_arr(self):
        self.i += 1  # [
        arr = []
        while True:
            self.skip_ws()
            if self.s[self.i] == ']':
                self.i += 1
                return arr
            arr.append(self.parse())
            self.skip_ws()
            c = self.s[self.i]
            if c == ',':
                self.i += 1
                self.skip_ws()
                if self.s[self.i] == ']':
                    self.i += 1
                    return arr
            elif c == ']':
                self.i += 1
                return arr
            else:
                raise ValueError(f"unexpected char {c!r} at {self.i}")

    def parse_str(self):
        q = self.s[self.i]
        self.i += 1
        out = []
        while self.i < self.n:
            c = self.s[self.i]
            if c == '\\':
                nxt = self.s[self.i+1]
                if nxt == 'x':
                    out.append(chr(int(self.s[self.i+2:self.i+4], 16)))
                    self.i += 4
                elif nxt == 'u':
                    out.append(chr(int(self.s[self.i+2:self.i+6], 16)))
                    self.i += 6
                elif nxt == 'n':
                    out.append('\n'); self.i += 2
                elif nxt == 't':
                    out.append('\t'); self.i += 2
                elif nxt == 'r':
                    out.append('\r'); self.i += 2
                else:
                    out.append(nxt); self.i += 2
            elif c == q:
                self.i += 1
                return ''.join(out)
            else:
                out.append(c)
                self.i += 1
        raise ValueError('unterminated string')

    def parse_identifier(self):
        start = self.i
        while self.i < self.n and (self.s[self.i].isalnum() or self.s[self.i] in '_$'):
            self.i += 1
        return self.s[start:self.i]

    def parse_word(self):
        start = self.i
        while self.i < self.n and self.s[self.i] not in ',}] \t\r\n':
            self.i += 1
        w = self.s[start:self.i].strip()
        if w == 'true':
            return True
        if w == 'false':
            return False
        if w in ('null', 'undefined', ''):
            return None
        try:
            if '.' in w or 'e' in w.lower():
                return float(w)
            return int(w)
        except ValueError:
            return w


def parse_js_object(text, start=0):
    p = JSParse(text, start)
    return p.parse()

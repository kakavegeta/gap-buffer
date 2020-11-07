
class TextEditor:
    def __init__(self, document, size = 10):
        self.document = document
        self.dictionary = set()
        with open("/usr/share/dict/words") as input_dictionary:
            for line in input_dictionary:
                words = line.strip().split(" ")
                for word in words:
                    self.dictionary.add(word)
        self.paste_text = []

        self.size = size # current buffer size
        self.buffer = ['*'] * self.size # use '_' fill gap
        self.gap_size = self.size 
        self.cursor_start = 0
        self.cursor_end = self.size - 1
        self._buffer_init(self.document)
    
    # initialize buffer
    def _buffer_init(self,chars):
        for i in range(len(chars)):
            self.buffer[self.cursor_start] = chars[i]
            self.cursor_start += 1
            if self.cursor_start > self.cursor_end:
                self.__resize()

    # as buffer is full, expand the buffer, and twice gap size
    def __resize(self):
        gap = ['*'] * self.gap_size
        self.buffer = self.buffer[:self.cursor_start] + gap + self.buffer[self.cursor_start:]
        self.size += self.gap_size
        self.gap_size *= 2
        #self.cursor_start += 1
        self.cursor_end = self.cursor_start + self.gap_size//2 - 1
        return
    
    # insert string before text_pos
    def insert_before(self, text_pos, chars):
        buf_pos = self._map(text_pos)
        if self.cursor_start > buf_pos:
            self._backward(buf_pos)
        elif self.cursor_end < buf_pos:
            buf_pos -= 1
            self._forward(buf_pos)
        for i in range(len(chars)):
            self.buffer[self.cursor_start] = chars[i]
            self.cursor_start += 1
            if self.cursor_start > self.cursor_end:
                self.__resize()
        #self.document = self.get_text()
        return
    
    # insert string after text_pos
    def insert_after(self, text_pos, chars):
        buf_pos = self._map(text_pos)
        if self.cursor_start > buf_pos:
            buf_pos += 1
            self._backward(buf_pos)
        elif self.cursor_end < buf_pos:
            self._forward(buf_pos)
        for i in range(len(chars)):
            self.buffer[self.cursor_start] = chars[i]
            self.cursor_start += 1
            if self.cursor_start > self.cursor_end:
                self.__resize()
        #self.document = self.get_text()
        return
    
    def get_text(self):
        return ''.join([''.join(self.buffer[:self.cursor_start]), ''.join(self.buffer[self.cursor_end+1:])])
    
    def _get_buffer(self):
        return ''.join(self.buffer)
    
    # move cursor_start to delete position, and increase cursor_end
    def delete(self, text_pos):
        buf_pos = self._map(text_pos)
        if self.cursor_start > buf_pos:
            self._backward(buf_pos)
            self.cursor_end += 1 # no need to change ch in buffer at cursor_start
        elif self.cursor_end < buf_pos:
            self._forward(buf_pos)
            self.cursor_start -= 1 # same as above
        #self.document = self.get_text()
        return

    # move cursor_start to pos
    def _backward(self, pos):
        while self.cursor_start > pos:
            self.cursor_start -= 1
            self.cursor_end -= 1
            self.buffer[self.cursor_end+1] = self.buffer[self.cursor_start]
            self.buffer[self.cursor_start] = '*'
        return

    # move cursor_end to pos 
    def _forward(self, pos):
        while self.cursor_end < pos:
            self.cursor_start += 1
            self.cursor_end += 1
            self.buffer[self.cursor_start-1] = self.buffer[self.cursor_end]
            self.buffer[self.cursor_end] = '*'
        return
    
    # map text pos to buffer pos
    def _map(self, text_pos):
        if text_pos < self.cursor_start:
            buf_pos = text_pos
        else:
            buf_pos = self.cursor_end + text_pos - self.cursor_start + 1
        return buf_pos
    
    def copy(self, i, j):
        self.paste_text = self.buffer[i:j]
        return
    
    # cut [start, stop)
    def cut(self, start, stop): 
        self.paste_text = self.buffer[start:stop]
        for _ in range(stop-start):
            self.delete(start)
        #self.document = self.get_text()
        return
    
    # given the original editor implement after-paste, here we follow the original design
    def paste(self, text_pos):
        paste_text = ''.join(self.paste_text)
        self.insert_after(text_pos, paste_text)
        #self.document = self.get_text()
        return

    def paste_before(self, text_pos):
        paste_text = ''.join(self.paste_text)
        self.insert_before(text_pos, paste_text)
        #self.document = self.get_text()
        return
    
    def misspellings(self):
        result = 0
        for word in self.document.split(" "):
            if word not in self.dictionary:
                result = result + 1
        return result


def test(editor):
    print("text: ", editor.get_text())
    print("buffer: ", editor._get_buffer())
    print("gap size: ", editor.gap_size)
    print("cursor start: ",editor.cursor_start)
    print("cursor end: " ,editor.cursor_end)
    print("#######################################")


def main():
    editor = MyEditor("HelloWorldHelloWo", 10)
    test(editor)
    '''
    editor._backward(3)
    test(editor)
    editor._forward(9)
    test(editor)
    editor.delete(15)
    test(editor)
    editor.delete(1)
    test(editor)
    editor.delete(0)
    test(editor)
    editor.insert_after(1, "Hello")
    test(editor)
    '''
    editor.copy(5,10)
    editor.paste(-1)
    test(editor)

    editor.cut(0, 5)
    test(editor)
    editor.paste(4)
    test(editor)


if __name__ == "__main__":
    main()
    





    



import pygame

class Level:
    def __init__(self):
        self.map = list()
        pass

    def refresh(self):
        pass

    def move(self, mousePos):
        pass

class Button:
    def __init__(self, pos, dim, colDef, colHov, rectBord, content, funDef):
        """
        The constructor for the Button object

        :param (int, int) pos: The x and y positions of the top left corner of the button
        :param (int, int)) dim: The width and height of the button in pixels
        :param (int, int, int) colDef: The default colour of the button
        :param (int, int, int) colHov: The hover colour of the button
        :param int rectBord: Size of rounded egdes on rectangle
        :param (text, text colour, text hover colour, text font, font size) OR (image, padding) content: The information to display on the button
        :param *Function fun: The reference to a function to call on button press
        :param (*) funPar: Parameters to pass into the object
        """

        # text, textCol, textHovCol, textFont, fontSize

        self.pos = pos
        self.dim = dim

        self.colourDefault = colDef
        self.colourHover = colHov

        self.borderSize = rectBord

        self.functionDefinition = funDef

        self.content = content

        if len(content) == 5:
            self.dataType = "text"

            self.text = content[0]
            self.textCol = content[1]
            self.textHovCol = content[2]
            self.textFont = content[3]
            self.fontSize = content[4]
        elif len(content) == 2:
            self.dataType = "image"

            self.image = content[0]
            self.padding = content[1]

    
    def press(self, ev):
        # if mouse is in the range of the button
        if self.mouseIn():
            if ev.type == pygame.MOUSEBUTTONDOWN:
                for x in self.functionDefinition:
                    if (ev.button == x):
                        self.functionDefinition[x][0](*(self.functionDefinition[x][1]))

    def draw(self, surface):
        colourBox = self.colourHover if self.mouseIn() else self.colourDefault

        curRect = pygame.Rect(self.pos, self.dim)
        pygame.draw.rect(surface, colourBox, curRect, border_radius = self.borderSize)

        if self.dataType == "text":
            colourText = self.textHovCol if self.mouseIn() else self.textCol

            text_rect = self.textFont.get_rect(self.text, size = self.fontSize)
            text_rect.center = curRect.center
            self.textFont.render_to(surface, text_rect, self.text, colourText, size = self.fontSize)
        elif self.dataType == "image":
            picture = self.image
            picture = pygame.transform.scale(picture, (self.dim[0] - self.padding, self.dim[1] - self.padding))
            rect = picture.get_rect()
            rect = rect.move((self.pos[0] + self.padding/2, self.pos[1] + self.padding/2))
            surface.blit(picture, rect)

    def mouseIn(self):
        mousePos = pygame.mouse.get_pos()
        return (mousePos[0] >= self.pos[0] and mousePos[0] <= self.pos[0] + self.dim[0]) and (mousePos[1] >= self.pos[1] and mousePos[1] <= self.pos[1] + self.dim[1])
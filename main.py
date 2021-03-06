import sys
import pygame
import time
import random
import threading

class Button:
    def __init__(self, sortApp, text, width, height, position, color, font):
        self.screen = sortApp.screen
        self.screenRect = self.screen.get_rect()

        #properti dan dimensi
        self.width, self.height = width, height
        self.buttonColor = color
        self.textColor = font[2]
        self.font = pygame.font.SysFont(font[0], font[1])

        #bikin objek rectangle dari button terus simpen di tengah bawah
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = position[0]
        self.rect.y = position[1]

        #The button message needs to be prepped only once.
        self._prep_msg(text)
    
    def _prep_msg(self, text):
        self.msg_image = self.font.render(text, True, self.textColor, self.buttonColor)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        #draw blank button and then draw message.
        self.screen.fill(self.buttonColor, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

class Sort_screen:
    def __init__(self, sortApp, width, height, border, color, border_color, position):
        self.screen = sortApp.screen
        self.x = position[0]
        self.y = position[1]
        self.color = color
        self.width = width
        self.height = height
        self.border = border
        self.border_color = border_color
        self.surf = pygame.Surface((self.width+self.border*2, self.height+self.border*2), pygame.SRCALPHA)
    
    def create_rect(self):
        pygame.draw.rect(self.surf, self.color, (self.border, self.border, self.width, self.height), 0)
        for i in range(1, self.border):
            pygame.draw.rect(self.surf, self.border_color, (self.border-i, self.border-i, self.width+5, self.height+5), 1)
        return self.surf
    
    def draw_rect(self):
        self.rect_surf1 = self.create_rect()
        self.screen.blit(self.rect_surf1, (self.x , self.y))

class SortSprite(pygame.sprite.Sprite):
    def __init__(self, dictRect):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((dictRect["width"], dictRect["height"]))
        self.image.fill(dictRect["color"])
        self.rect = self.image.get_rect()
        self.rect.x = dictRect["posX"]
        self.rect.y = dictRect["posY"]
    
    def update(self, key, value):
        if key == "color":
            self.image.fill(value)
        elif key == "width":
            self.rect.width = value


class Sort_Object:
    def __init__(self, sortApp, position, color, maxwidth, maxheight):
        self.screen = sortApp.screen
        self.nilaimax = sortApp.nilaimax
        self.start_x = position[0]
        self.start_y = position[1]
        self.color = color
        self.maxwidth = maxwidth-3
        self.maxheight = float(maxheight-3)
        self.list_object = self.generate_list_of_rect()
        self.list_of_rect = self.generate_rect()
        

    def generate_list_of_rect(self):
        self.list_object = []
        random.seed(5)
        partHeight = self.maxheight/self.nilaimax
        for i in range(0, self.nilaimax):
            partWidth = random.randint(2, self.maxwidth-1)
            if i == 0:
                posX = float(self.start_x)
                posY = float(self.start_y)
            else:
                posY += partHeight
            self.list_object.append({"width": partWidth, "color": self.color, "height": partHeight,"posX": posX,"posY": posY})
        return self.list_object
    
    def generate_rect(self):
        self.list_of_rect = []
        for i in self.list_object:
            sprite = SortSprite(i)
            sgrup = pygame.sprite.RenderUpdates(sprite)
            self.list_of_rect.append(sgrup)
        return self.list_of_rect
            
    def draw_sort(self):
        for i in self.list_of_rect:
            i.draw(self.screen)

class Selection(pygame.sprite.Sprite):
    def __init__(self, sortApp, defaultColor):
        pygame.sprite.Sprite.__init__(self)
        self.sortApp = sortApp
        self.running_time = 0.0
        self.color = (0, 0, 0)
        self.image = pygame.surface.Surface((320, 500))
        self.rect = self.image.get_rect()
        self.rect.x = 25
        self.rect.y = 85
        self.bg_color = sortApp.bg_color
        self.screen = sortApp.screen
        self.sel_listObject = sortApp.sel_list
        self.sel_listOfRect = sortApp.sel_rect
        self.defaultColor = defaultColor
        self.surf = pygame.Surface((320, 500), pygame.SRCALPHA)

    def sel_draw_obj(self, index):
        
        temp_s = SortSprite(self.sel_listObject[index])
        self.sel_listOfRect[index].empty()
        self.sel_listOfRect[index].add(temp_s)
        self.change_rect2 = pygame.Rect(25, 85, 325, 505)
        pygame.draw.rect(self.surf,self.bg_color, self.surf.get_rect())
        self.screen.blit(self.surf, (self.rect.x, self.rect.y))
        self.temp_group = pygame.sprite.RenderUpdates()
        
        for i in self.sel_listOfRect:
            self.temp_group.add(i)
        self.temp_group.draw(self.screen)

    
    def update(self):
        start = time.perf_counter()
        self.size = len(self.sel_listObject)
        for step in range(self.size):
            min_idx = step
            #self.sel_listObject[step]["color"] = (0, 0, 0)
            #self.sel_draw_obj(step)
            for i in range(step + 1, self.size):
                #self.sel_listObject[i]["color"] = (255, 255, 255)
                #self.sel_draw_obj(i)
                #self.sel_listObject[min_idx]["color"] = (0, 0, 0)
                #self.sel_draw_obj(min_idx)
                #self.sel_listOfRect[min_idx].update("color", (0, 0, 0))
                if self.sel_listObject[i]["width"] < self.sel_listObject[min_idx]["width"]:
                    #self.sel_listObject[min_idx]["color"] = self.defaultColor
                    #self.sel_draw_obj(min_idx)
                    min_idx = i
                    #self.sel_listObject[min_idx]["color"] = (0, 0, 0)
                    #self.sel_draw_obj(min_idx)
                #self.sel_listObject[i]["color"] = self.defaultColor
                self.sel_draw_obj(i)
            #temp_index = step
            t = self.sel_listObject[step]["width"]
            self.sel_listObject[step]["width"] = self.sel_listObject[min_idx]["width"]
            self.sel_listObject[min_idx]["width"] = t
            self.sel_draw_obj(step)
            self.sel_draw_obj(min_idx)
            #self.sel_listObject[temp_index]["color"] = self.defaultColor
            #self.sel_draw_obj(temp_index)
        finish = time.perf_counter()
        self.running_time = round(finish-start, 10)
        print("Running time selection sort:", self.running_time)

class Insertion(pygame.sprite.Sprite):
    def __init__(self, sortApp, defaultColor):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.surface.Surface((325, 505))
        self.running_time = 0.0
        self.rect = self.image.get_rect()
        self.rect.x = sortApp.ins_dinst+5
        self.rect.y = 85
        self.sortApp = sortApp
        self.color = (0, 0, 0)
        self.bg_color = sortApp.bg_color
        self.screen = sortApp.screen
        self.ins_listObject = sortApp.ins_list
        self.ins_listOfRect = sortApp.ins_rect
        self.defaultColor = defaultColor
        self.surf = pygame.Surface((320, 500), pygame.SRCALPHA)

    def ins_draw_obj(self, index):
        temp_s = SortSprite(self.ins_listObject[index])
        self.ins_listOfRect[index].empty()
        self.ins_listOfRect[index].add(temp_s)
        self.change_rect = pygame.Rect(self.sortApp.ins_dinst+5, 85, 325, 505)
        pygame.draw.rect(self.surf,self.bg_color, self.surf.get_rect())
        self.screen.blit(self.surf, (self.rect.x, self.rect.y))
        self.temp_group = pygame.sprite.RenderUpdates()
        for i in self.ins_listOfRect:
            self.temp_group.add(i)
        self.temp_group.draw(self.screen)

    def update(self):
        start = time.perf_counter()
        self.size = len(self.ins_listObject)  
        for i in range(1, self.size): 
            key = self.ins_listObject[i]["width"] 
            #self.ins_listObject[i]["color"] = (0, 0, 0)
            #self.ins_draw_obj(i)
            j = i-1
            while j >= 0 and key < self.ins_listObject[j]["width"]  :
                    #self.ins_listObject[j]["color"] = (0, 0, 0)
                    #self.ins_draw_obj(i) 
                    self.ins_listObject[j + 1]["width"] = self.ins_listObject[j]["width"]
                    self.ins_draw_obj(j+1)
                    #self.ins_listObject[j]["color"] = self.defaultColor
                    #self.ins_draw_obj(i) 
                    j -= 1
            #self.ins_listObject[i]["color"] = self.defaultColor
            self.ins_draw_obj(i)
            self.ins_listObject[j + 1]["width"] = key
            self.ins_draw_obj(j+1)
        finish = time.perf_counter()
        self.running_time = round(finish-start, 10)
        print("Running time insertion sort:", self.running_time)
        
            

class Echidna:
    def __init__(self):
        pygame.init()
        self.width = 720
        self.height = 720
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Selection and Insertion Sorting Algorithm Visualizer")
        self.bg_color = (230, 230, 230)
        self.selection_screen = Sort_screen(self, 320, 500, 5, self.bg_color, (0, 0, 0), (20, 80))
        self.sel_surf = self.selection_screen.surf.get_rect()
        self.ins_dinst = 30+self.selection_screen.width+20
        self.insertion_screen = Sort_screen(self, 320, 500, 5, self.bg_color, (0, 0, 0), (self.ins_dinst, 80))
        self.ins_surf = self.insertion_screen.surf.get_rect()
        self.nilaimax = 100
        self.selection_obj = Sort_Object(self, (25, 85), (4, 133, 253), self.selection_screen.width, self.selection_screen.height)
        self.insertion_obj = Sort_Object(self, (35+self.selection_screen.width+20, 85), (4, 133, 253), self.insertion_screen.width, self.insertion_screen.height)
        self.sel_rect = self.selection_obj.list_of_rect
        self.ins_rect = self.insertion_obj.list_of_rect
        self.sel_list = self.selection_obj.list_object
        self.ins_list = self.insertion_obj.list_object
        self.sel_sorting = Selection(self, (4, 133, 253))
        self.ins_sorting = Insertion(self, (4, 133, 253))
        self.spriteSort = pygame.sprite.RenderUpdates(self.sel_sorting)
        self.spriteSort2 = pygame.sprite.RenderUpdates(self.ins_sorting)
        #self.clock = pygame.time.Clock()
        #button
        self.sort_button = Button(self, "Sort", 200, 50, (self.screen.get_rect().centerx-100,self.height-10-80), (0, 0, 0), ("Arial", 30, (255, 255, 255)))
        self.sel_title = Button(self, "Selection", 200, 50, (75,25), self.bg_color, ("Arial", 32, (0, 0, 0)))
        self.ins_title = Button(self, "Insertion", 200, 50, (self.selection_screen.width+30+75,25), self.bg_color, ("Arial", 32, (0, 0, 0)))
        #self.runtime_sel = Button(self, "Running time: "+str(self.sel_sorting.running_time),200, 50,  (self.screen.get_rect().centerx-100,self.height-10-100), self.bg_color, ("Arial", 16, (0, 0, 0)))
        #self.runtime_ins = Button(self, "Running time: "+str(self.ins_sorting.running_time),200, 50,  (self.screen.get_rect().centerx+100,self.height-10-100), self.bg_color, ("Arial", 16, (0,0,0)))

    def run_app(self):
        while True:
            self._check_events()
            self._update_screen()
            
    
    def _check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                button_clicked = self.sort_button.rect.collidepoint(mouse_pos)
                if button_clicked:
                    self.spriteSort.draw(self.screen)
                    self.spriteSort2.draw(self.screen)
                    t1 = threading.Thread(target=self.spriteSort.update)
                    t2 = threading.Thread(target=self.spriteSort2.update)
                    t1.start()
                    t2.start()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    self.sel_sorting.selection_sort()
                if event.key == pygame.K_w:
                    self.sel_sorting.insertionSort()
                

    #def _check_button(self, mouse_pos):
    def _reset_screen_without_sortObj(self):
        self.screen.fill(self.bg_color)
        self.selection_screen.draw_rect()
        self.insertion_screen.draw_rect()
        self.sort_button.draw_button()
        self.sel_title.draw_button()
        self.ins_title.draw_button()
        

    def _update_screen(self):
        self._reset_screen_without_sortObj()
        self.selection_obj.draw_sort()
        self.insertion_obj.draw_sort()
        pygame.display.flip()

if __name__ == '__main__':
    echidna = Echidna()
    echidna.run_app()
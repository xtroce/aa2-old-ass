__author__ = 'fbuettner'
import Tkinter as tk
import time

import pkg_resources

from models.field import Field
from models.predator import Predator
from models.prey import Prey
from models.state import State


class GameFrame(tk.Frame):
    def __init__(self, master=None, field=None, window_title=None):
        tk.Frame.__init__(self, master)
        self.root = tk.Tk()
        self.master.title(window_title if window_title is not None else "AA1-GUI")
        self.field = field
        self.rows = self.field.height
        self.columns = self.field.width
        self.xoffset = self.yoffset = 20
        self.cellwidth = 50
        self.cellheight = 50
        self.width = (2 * self.xoffset) + (self.rows * self.cellwidth)
        self.height = (2 * self.yoffset) + (self.columns * self.cellheight)
        self.state = dict()
        self.grid()
        self.create_field_grid()
        self.create_icons()
        self.root.update()
        self.root.after(25)
        # self.draw_state(state=((1, 1), (5, 5)), trace=False)
        # self.draw_state(state=((1, 3), (7, 5)), trace=True)
        #self.draw_state(state=((0, 3), (7, 0)), trace=True)

    def update(self, trace=True):
        self.draw_state(state=self.field.get_current_state_complete(), trace=trace)


    def create_widgets(self):
        self.quitButton = tk.Button(self, text="Quit", command=self.quit)
        self.quitButton.grid()

    def create_field_grid(self):
        self.canvas = tk.Canvas(self, width=self.width, height=self.height, borderwidth=0, highlightthickness=0)
        self.canvas.pack(side="top", fill="both", expand="true")
        for row in range(self.rows):
            for column in range(self.columns):
                x1 = self.xoffset + row * self.cellheight
                x2 = x1 + self.cellheight
                y1 = self.yoffset + column * self.cellwidth
                y2 = y1 + self.cellwidth
                self.canvas.create_rectangle(x1, y1, x2, y2)

    def create_icons(self):
        self.players = dict()
        self.predator_icon = tk.PhotoImage(file=pkg_resources.resource_filename('graphics.gui', 'images/predator.gif'))
        self.prey_icon = tk.PhotoImage(file=pkg_resources.resource_filename('graphics.gui', 'images/prey.gif'))
        for player in self.field.get_players():
            self.state[player] = player.location
            if isinstance(player, Predator):
                self.players[player] = self.canvas.create_image(self.xoffset, self.yoffset, anchor="nw", image=self.predator_icon)
            else:
                self.players[player] = self.canvas.create_image(self.xoffset, self.yoffset, anchor="nw", image=self.prey_icon)
        self.prey_dead_icon = tk.PhotoImage(
            file=pkg_resources.resource_filename('graphics.gui', 'images/prey_dead.gif'))
        self.state = {player: (0,0) for player in self.field.get_players()}
        self.update(trace=False)
        return None

    def update(self, trace=False, keep_open=False):
        """
        Updates the positions of th player icons according to the field state.
        :param trace: draw a trace of the past movements of each player
        :param keep_open: keep the window open after the episode has ended
        :return: None
        """
        if trace:
            # # predator trace
            # start = self.get_field_center(predator_location_old[0], predator_location_old[1])
            # end = self.get_field_center(predator_location_new[0], predator_location_new[1])
            # # add +1 to separate from blue line
            # self.canvas.create_line(start.get("x") + 1, start.get("y") + 1, end.get("x") + 1, end.get("y") + 1,
            #                         fill="red")
            # # prey trace
            # start = self.get_field_center(prey_location_old[0], prey_location_old[1])
            # end = self.get_field_center(prey_location_new[0], prey_location_new[1])
            # # subtract -1 to separate from red line (1px in between)
            # self.canvas.create_line(start.get("x") - 1, start.get("y") - 1, end.get("x") - 1, end.get("y") - 1,
            #                         fill="blue")
            pass
        for player in self.field.get_players():
            player_dx = player.location[0] - self.state[player][0]
            player_dy = player.location[1] - self.state[player][1]
            self.canvas.move(self.players[player], player_dx * self.cellwidth, player_dy * self.cellheight)
            self.state[player] = player.location
        if self.field.is_ended():
            # draw all the fields red where multiple players stand
            pass
            #     x1 = self.xoffset + predator_location_new[0] * self.cellheight
            #     x2 = x1 + self.cellheight
            #     y1 = self.yoffset + predator_location_new[1] * self.cellwidth
            #     y2 = y1 + self.cellwidth
            #     self.canvas.create_rectangle(x1, y1, x2, y2, fill="#F0AFBB")
            #     self.canvas.create_image(x1, y1, anchor="nw", image=self.prey_dead_icon)
            if keep_open:
                self.mainloop()
        self.root.update()
        return None

    def get_field_center(self, col, row):
        """
        calculates the x and y pixel coordinates of the field at given column and row in the grid.
        :param col:
        :param row:
        :return: dictionary with elements x and y
        """
        x = self.xoffset + col * self.cellwidth + 0.5 * self.cellwidth
        y = self.yoffset + row * self.cellheight + 0.5 * self.cellheight
        return {"x": x, "y": y}


if __name__ == "__main__":
    environment = Field(11, 11)
    # fatcat = Predator((0, 0))
    # fatcat.policy = RandomPredatorPolicy(fatcat, environment)
    # chip = Prey((5, 5))
    # chip.policy = RandomPreyPolicy(chip, environment)
    # environment.add_player(fatcat)
    # environment.add_player(chip)
    # gui = GameFrame(field=environment)
    # gui.draw_state(environment.get_current_state_complete())
    # i = 0
    # while not environment.is_ended():
    #     fatcat.act()
    #     chip.act()
    #     # print environment
    #     gui.update()
    #     i += 1
    #     time.sleep(0.1)
    # gui.mainloop()
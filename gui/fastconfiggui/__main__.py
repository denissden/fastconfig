import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext as st
import requests
import urllib.parse
import json
import os


CONFIG_FILE = os.path.join(os.path.expanduser("~"), ".config", "fastconfig.json")
URL_SHEME = "http"

def DEFAULT_CONFIG():
    c = Config(CONFIG_FILE)
    c.put(400, "window", "x")
    c.put(300, "window", "y")
    c.put({
        "address": "",
        "app_id": "",
        "token": ""
    }, "envs", "local")
    return c


def config_entry(address, app_id, token):
    return {
            "address": address,
            "app_id": app_id,
            "token": token,
        }


class Config:
    def __init__(self, path: str, default="") -> None:
        self.path = path
        self.default = default
        self.config = dict()

        self.load()
    
    def get(self, *args, default=None):
        section = self.config
        for a in args:
            section = self.tryget(section, a)
            if section is None:
                return self.default if default is None else default
        return section
    
    def get_config(self, *args):
        v = self.get(*args)
        c = Config(None)
        c.config = v
        return c

    def put(self, value, *args):
        section = self.config
        for a in args[:-1]:
            next_ = self.tryget(section, a)
            if next_ is None:
                section[a] = dict()
            else:
                section[a] = next_
            section = section[a]
        section[args[-1]] = value
    
    def load(self):
        if self.config is None:
            self.config = dict()
            return
        try:
            with open(self.path) as f:
                self.config = json.load(f)
        except Exception:
            self.config = dict()
    
    def save(self):
        with open(self.path, "w+") as f:
            json.dump(self.config, f, indent=4)
    
    @staticmethod
    def tryget(d, key):
        if d is not None and key in d:
            return d[key]
        else:
            return None


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.config = Config(CONFIG_FILE)
        self.environment = None

        size_x = self.config.get("window", "x", default=400)
        size_y = self.config.get("window", "y", default=300)
        self.geometry(f"{size_x}x{size_y}")
        self.resizable(False, False)
        self.title("FastConfig client")

        self.tv_env = tk.StringVar()
        self.tv_address = tk.StringVar()
        self.tv_app_id = tk.StringVar()
        self.tv_token = tk.StringVar()
        self.tv_send = tk.StringVar()
        self.tv_get = tk.StringVar()

        self.envs = [k for k in self.config.get("envs", default=dict()).keys()]
        
        self.protocol("WM_DELETE_WINDOW", self.on_close)
        self.setup_ui()

        if self.envs:
            self.set_env(self.envs[0])


    def setup_ui(self):
        self.f_env = ttk.Frame()
        for i, env in enumerate(self.envs):
            b = ttk.Button(self.f_env, text=env, command=lambda env=env: self.set_env(env))
            b.grid(column=i, row=1)
        # self.cmb_env = ttk.Combobox(self.f_env, values=envs, textvariable=self.tv_env)
        # self.cmb_env.bind("<<ComboboxSelected>>", self.env_selected)
        # self.cmb_env.pack()
        self.f_env.pack()

        self.f_values = ttk.Frame()
        self.l_addr = ttk.Label(self.f_values, text="Address")
        self.l_addr.grid(column=0, row=0)
        self.t_addr = ttk.Entry(self.f_values, textvariable=self.tv_address)
        self.t_addr.grid(column=1, row=0)
        self.l_app_id = ttk.Label(self.f_values, text="App id: ")
        self.l_app_id.grid(column=0, row=1)
        self.t_app_id = ttk.Entry(self.f_values, textvariable=self.tv_app_id)
        self.t_app_id.grid(column=1, row=1)
        self.l_token = ttk.Label(self.f_values, text="Token: ")
        self.l_token.grid(column=0, row=2)
        self.t_token = ttk.Entry(self.f_values, textvariable=self.tv_token)
        self.t_token.grid(column=1, row=2)
        self.f_values.pack()

        self.f_fields = ttk.Frame()
        self.t_request = st.ScrolledText(self.f_fields, wrap=tk.CHAR, height=5)
        self.t_request.grid(column=0, row=0)
        self.t_response = st.ScrolledText(self.f_fields, height=5)
        self.t_response.grid(column=1, row=0)
        self.f_fields.grid_columnconfigure(0, weight=1)
        self.f_fields.grid_columnconfigure(1, weight=1)
        self.btn_send = ttk.Button(self.f_fields, text="Send config", command=self.send)
        self.btn_send.grid(column=0, row=1, sticky="nsew")
        self.btn_send = ttk.Button(self.f_fields, text="Get config", command=self.get)
        self.btn_send.grid(column=1, row=1, sticky="nsew")
        self.btn_send = ttk.Button(self.f_fields, text="Paste", command=self.paste_request)
        self.btn_send.grid(column=0, row=2, sticky="nsew")
        self.btn_send = ttk.Button(self.f_fields, text="Copy", command=self.copy_response)
        self.btn_send.grid(column=1, row=2, sticky="nsew")
        self.f_fields.pack()

    @property
    def headers(self):
        return {
            "token": self.tv_token.get()
        }
    
    @property
    def root_address(self):
        url_to_check = self.tv_address.get()
        if not url_to_check.startswith("http"):
            return f"{URL_SHEME}://{url_to_check}"
        return url_to_check

    @property
    def config_address(self):
        first_part = urllib.parse.urljoin(
            self.root_address, 
            "configuration")
        return f"{first_part}/{self.tv_app_id.get()}"

    @property
    def request_text(self):
        return self.t_request.get("1.0", tk.END)
    
    @request_text.setter
    def request_text(self, v):
        self.t_request.delete("1.0", tk.END)
        return self.t_request.insert(tk.END, v)

    @property
    def response_text(self):
        return self.t_response.get("1.0", tk.END)
    
    @response_text.setter
    def response_text(self, v):
        self.t_response.delete("1.0", tk.END)
        return self.t_response.insert(tk.END, v)

    def send(self):
        addr = self.config_address
        body = self.request_text
        resp = requests.put(addr, body, headers=self.headers)
        self.response_text = resp.text

    def get(self):
        resp = requests.get(self.config_address, headers=self.headers)
        self.response_text = resp.text
    
    def set_env(self, env):
        if self.environment is not None:
            self.save_values()

        self.environment = env
        env_conf = self.config.get_config("envs", self.environment)
        self.tv_address.set(env_conf.get("address"))
        self.tv_app_id.set(env_conf.get("app_id"))
        self.tv_token.set(env_conf.get("token"))

    def save_values(self):
        to_save = config_entry(
            str(self.tv_address.get()),
            str(self.tv_app_id.get()),
            str(self.tv_token.get())
        )
        env = self.environment
        self.config.put(to_save, "envs", env)
        self.config.save()

    def copy_response(self):
        self.clipboard_clear()
        self.clipboard_append(self.response_text)
    
    def paste_request(self):
        request = self.clipboard_get()
        self.request_text = request
    
    def on_close(self):
        self.config.save()
        self.quit()

if __name__ == '__main__':
    if not os.path.exists(CONFIG_FILE):
        c = DEFAULT_CONFIG()
        c.save()

    app = App()
    app.mainloop()
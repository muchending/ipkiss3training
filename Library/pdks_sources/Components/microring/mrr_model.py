from si_fab import all as pdk
from ipkiss3 import all as i3
import numpy as np  # useful numerical package
import json


class mrr_model(i3.CompactModel):
        parameters = ["center_wavelength",
                      "through_response",
                      "drop_response",
                      "reflection_in1",
                      "reflection_in2",
                      "reflection_out1",
                      "reflection_out2",

        ]
        terms = [i3.OpticalTerm(name="input"),
                 i3.OpticalTerm(name="through"),
                 i3.OpticalTerm(name="add"),
                 i3.OpticalTerm(name="drop"),
        ]
        def calculate_smatrix(parameters,env,S):
            through_response = np.polyval(parameters.through_response,env.wavelength-parameters.center_wavelength)
            drop_response=np.polyval(parameters.drop_response,env.wavelength-parameters.center_wavelength)
            reflection_in1=np.polyval(parameters.reflection_in1,env.wavelength-parameters.center_wavelength)
            reflection_in2=np.polyval(parameters.reflection_in2,env.wavelength-parameters.center_wavelength)
            reflection_out1 = np.polyval(parameters.reflection_out1, env.wavelength - parameters.center_wavelength)
            reflection_out2 = np.polyval(parameters.reflection_out2, env.wavelength - parameters.center_wavelength)

            # Add-Drop 微环 S 参数定义（16个元素完整定义）

            # 1. 传输路径（互为互易，成对赋值）
            S["input", "through"] = S["through", "input"] = through_response  # 直通端
            S["input", "drop"] = S["drop", "input"] = drop_response  # 下载端
            S["add", "drop"] = S["drop", "add"] = through_response  # 添加端直通（对称）
            S["add", "through"] = S["through", "add"] = drop_response  # 反向下载（对称）

            # 2. 反射系数（各端口独立，理想情况全为0）
            S["input", "input"] = reflection_in1
            S["through", "through"] = reflection_out1
            S["add", "add"] = reflection_in2
            S["drop", "drop"] = reflection_out2

            # 3. 非相邻端口串扰（理想波导无直接耦合，设为0）
            S["input", "add"] = S["add", "input"] = 0
            S["input", "drop"] = S["drop", "input"] = 0  # 注意：这里与 drop_response 不同，此项特指非谐振时的泄露
            S["through", "drop"] = S["drop", "through"] = 0
            S["through", "add"] = S["add", "through"] = 0


import flet as ft
import time
import serial

ser = serial.Serial('COM5', 9600, timeout=1)
time.sleep(2)

def main(page):
    page.theme_mode = ft.ThemeMode.LIGHT
    
    slider_values = [90, 0, 0, 90, 0]
    moviment_value = 0
    saved_properties = (slider_values)
    sliders = []
    segmented_button = None
    segmented_button_moviment = None
    stop_movement = False

    bottom_sheet = ft.BottomSheet(content=ft.Container(padding=20), open=False)
    page.overlay.append(bottom_sheet)

    def send_servo_value(servo_id, value):
        # Certifica-se de que o valor seja inteiro
        value = int(value)
        command = f'{servo_id},{value}\n'
        ser.write(command.encode('utf-8'))
        print(f"Enviando para servo {servo_id}: {value}")


    def get_values():
        # Retorna os valores como inteiros
        return [int(slider.value) for slider in sliders]


    def handle_change(e):
        slider_id = e.control.data
        value = int(e.control.value)  # Certifica-se que o valor é inteiro
        send_servo_value(slider_id, value)


    def handle_button_change2(e):
        nonlocal moviment_value
        # Remove colchetes e aspas antes de converter
        moviment_value = int(e.data.strip('[]').strip('"'))
        page.update()

    def save_properties(e):
        global saved_properties
        slider_values = get_values()
        saved_properties = (slider_values.copy())
        print(f"Propriedades salvas: {saved_properties}")
        page.update()

    def reset_positions(e):
        slider_values = [90, 0, 0, 90, 0]
        # Atualiza os sliders
        for i, slider in enumerate(sliders):
            slider.value = slider_values[i]
            send_servo_value(i + 1, slider.value)  # Envia o valor para o servo correspondente
        if segmented_button_moviment:
            segmented_button_moviment.selected = {moviment_value}
        
        page.update()

    def save_properties_long_press(e):
        global saved_properties
        slider_values = get_values()
        saved_properties = (slider_values.copy())
        print(f"Propriedades salvas: {saved_properties}")
        show_bottom_sheet(f"Propriedades salvas: {saved_properties}")  # Mostrar no BottomSheet
        page.update()

    def show_bottom_sheet(content):
        bottom_sheet.content = ft.Container(ft.Text(content, size=20), padding=20)
        bottom_sheet.open = True
        page.update()

    def write_positions(e):
        try:
            linha_escolhida = int(moviment_value)
            if linha_escolhida < 0 or linha_escolhida > 2:
                show_bottom_sheet(f"Erro: O valor de linha {linha_escolhida} não é permitido.")
                return
            
            linhas = handle_file('read')
            while len(linhas) <= linha_escolhida:
                linhas.append("\n")
            linhas = [linha.strip() for linha in linhas]

            # Obter os valores atuais dos sliders
            slider_values = get_values()  # Atualiza aqui

            linhas[linha_escolhida] = f"{slider_values}"
            with open('posicoes.txt', 'w') as arquivo:
                for linha in linhas:
                    arquivo.write(f"{linha}\n")
            
            show_bottom_sheet(f'Valores exportados: {slider_values}, (linha {linha_escolhida + 1})')
            print(f'Conteúdo escrito na linha {linha_escolhida + 1} com sucesso em posicoes.txt.')
        except Exception as ex:
            show_bottom_sheet(f'Ocorreu um erro: {ex}')

    def play_movements(e):
        global stop_movement
        stop_movement = False
        try:
            with open("posicoes.txt", 'r') as arquivo:
                linhas = arquivo.readlines()

            for linha in linhas:
                if stop_movement:
                    break
                linha = linha.strip()
                if not linha:
                    continue
                
                # Remove colchetes e converte a linha em uma lista de floats
                sliders_str = linha.strip('[]')  # Remove colchetes da linha
                try:
                    slider_values = [int(float(value.strip())) for value in sliders_str.split(',')]
                except ValueError as ve:
                    print(f"Erro: Não foi possível converter os valores dos sliders. Detalhes do erro: {ve}")
                    continue
                
                # Atualiza os sliders e envia os valores para os servos
                for i, slider in enumerate(sliders):
                    slider.value = slider_values[i]
                    send_servo_value(i + 1, slider.value)  # Envia o valor para o servo correspondente
                    page.update()                
                # Envia o valor para o servo 5 se houver um valor a ser enviado
                if len(linhas) > 0:
                    button_value = 0  # Valor padrão ou ajuste conforme necessário
                    send_servo_value(5, button_value)  # Ajuste conforme necessário para o valor do botão

                if segmented_button:
                    segmented_button.selected = {button_value}
                time.sleep(3)  # Tempo entre movimentos

        except FileNotFoundError:
            print('O arquivo posicoes.txt não foi encontrado.')
        except Exception as ex:
            print(f'Ocorreu um erro: {ex}')

    def stop_movement_func(e):
        global stop_movement
        stop_movement = True
        print('Movimento parado.')

    def import_positions(e):
        nonlocal slider_values, moviment_value
        try:
            linha_escolhida = int(moviment_value)
            if linha_escolhida < 0 or linha_escolhida > 2:
                print(f"Erro: O valor de linha {linha_escolhida} não é permitido.")
                return

            linhas = handle_file('read')
            if linha_escolhida >= len(linhas):
                print(f"Erro: Não há dados suficientes no arquivo para a linha {linha_escolhida}.")
                return

            # Remove espaços em branco e formatação desnecessária
            linha = linhas[linha_escolhida].strip()
            sliders_str = linha.strip('[]')  # Remove colchetes da linha

            # Limpeza dos dados antes de converter
            slider_values = [int(float(value.strip())) for value in sliders_str.split(',')]
            
            # Atualiza os sliders e envia os valores para os servos
            for i, slider in enumerate(sliders):
                slider.value = slider_values[i]
                slider.update()  # Atualiza o slider na interface
                send_servo_value(i + 1, slider.value)  # Envia o valor importado para o servo correspondente

            # Atualiza a página após alterar todos os sliders
            page.update()

            print('As posições foram importadas e enviadas para os servos com sucesso.')

        except FileNotFoundError:
            print('O arquivo posicoes.txt não foi encontrado.')
        except Exception as ex:
            print(f'Ocorreu um erro: {ex}')

    def handle_file(operation):
        if operation == 'read':
            with open('posicoes.txt', 'r') as arquivo:
                return arquivo.readlines()
        elif operation == 'write':
            with open('posicoes.txt', 'w') as arquivo:
                return arquivo.readlines()
        return []

    slider0 = ft.Slider(min=0, max=180, width=300, value=90, data=1, on_change=handle_change, label="{value}º", adaptive=True)
    slider1 = ft.Slider(min=0, max=180, width=300, value=0, data=2, on_change=handle_change, label="{value}º", adaptive=True)
    slider2 = ft.Slider(min=0, max=180, width=300, value=0, data=3, on_change=handle_change, label="{value}º", adaptive=True)
    slider3 = ft.Slider(min=0, max=180, width=300, value=90, data=4, on_change=handle_change, label="{value}º", adaptive=True)
    slider4 = ft.Slider(min=0, max=90, width=300, value=0, data=5, on_change=handle_change, label="{value}º", adaptive=True)
    sliders = [slider0, slider1, slider2, slider3, slider4]

    def create_segmented_button_moviment():
        nonlocal segmented_button_moviment
        segmented_button_moviment = ft.SegmentedButton(
            on_change=handle_button_change2,
            selected={moviment_value},
            width=300,
            allow_multiple_selection=False,
            segments=[
                ft.Segment(value=0, label=ft.Text("1"), icon=ft.Icon(ft.icons.LOOKS_ONE)),
                ft.Segment(value=1, label=ft.Text("2"), icon=ft.Icon(ft.icons.LOOKS_TWO)),
                ft.Segment(value=2, label=ft.Text("3"), icon=ft.Icon(ft.icons.LOOKS_3)),
            ]
        )
        return segmented_button_moviment

    page.add(
        ft.Container(
            ft.Row([ft.Image(src="imagens/ufcat3.png", width=200, height=200, fit=ft.ImageFit.CONTAIN),
                        ft.Image(src="imagens/banner_ppgmo_23bbfad3fa.png", width=600, height=200, fit=ft.ImageFit.CONTAIN),
                        ft.Image(src="imagens/imtec_logo-removebg-preview.png", width=200, height=200, fit=ft.ImageFit.CONTAIN),
                        ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        ),
        ft.Container(
            ft.Row([ft.Column([ft.ElevatedButton(text="SAVE POSITIONS", on_click=save_properties, on_long_press=save_properties_long_press, width=300, height=80, style=ft.ButtonStyle(bgcolor=ft.colors.BLACK, color=ft.colors.WHITE, shape=ft.ContinuousRectangleBorder(radius=0))),
                            ft.ElevatedButton(text="PLAY MOVEMENTS", on_click=play_movements, width=300, height=80, style=ft.ButtonStyle(bgcolor=ft.colors.BLACK, color=ft.colors.WHITE, shape=ft.ContinuousRectangleBorder(radius=0))),
                            ft.ElevatedButton(text="STOP MOVEMENT", on_click=stop_movement_func, width=300, height=80, style=ft.ButtonStyle(bgcolor=ft.colors.BLACK, color=ft.colors.WHITE, shape=ft.ContinuousRectangleBorder(radius=0))),
                                ], alignment=ft.MainAxisAlignment.CENTER, height=600),
                ft.Column([ft.Image(src="imagens/braço.png", width=300, height=300, fit=ft.ImageFit.CONTAIN),]),
                ft.Column([ft.Row([slider0]),
                            ft.Row([slider1]),
                            ft.Row([slider2]),
                            ft.Row([slider3]),
                            ft.Row([slider4]),
                            ft.Row([create_segmented_button_moviment()])
                            ], alignment=ft.MainAxisAlignment.CENTER, height=600),
                ft.Column([ft.ElevatedButton(text="EXPORT POSITION", on_click=write_positions, width=300, height=80,
                                                style=ft.ButtonStyle(bgcolor=ft.colors.BLACK, color=ft.colors.WHITE, shape=ft.ContinuousRectangleBorder(radius=0))),
                            ft.ElevatedButton(text="IMPORT POSITIONS", on_click=import_positions, width=300, height=80,
                                                style=ft.ButtonStyle(bgcolor=ft.colors.BLACK, color=ft.colors.WHITE, shape=ft.ContinuousRectangleBorder(radius=0))),
                            ft.ElevatedButton(text="RESET POSITIONS", on_click=reset_positions, width=300, height=80,
                                                style=ft.ButtonStyle(bgcolor=ft.colors.BLACK, color=ft.colors.WHITE, shape=ft.ContinuousRectangleBorder(radius=0)))
                            ], alignment=ft.MainAxisAlignment.CENTER, height=600),
                ], alignment=ft.MainAxisAlignment.SPACE_AROUND),
        )
    )

ft.app(main)
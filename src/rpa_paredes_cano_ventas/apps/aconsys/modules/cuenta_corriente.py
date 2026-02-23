from uiautomation import WindowControl
from time import sleep
from contabot_ventas.aconsys.ocr_utils import  ocr_todo

class CuentaCorriente:
    def __init__(self, ventana_cuenta_corriente: WindowControl):
        self.ventana_cuenta_corriente: WindowControl = ventana_cuenta_corriente
    def obtener_cuentas_y_codigo(self, codigo_filter:str, razon_social:str) ->dict:
        window = self.ventana_cuenta_corriente.GetAncestorControl(lambda c, d: isinstance(c, WindowControl))
        barra_vuenta_corriente = self.ventana_cuenta_corriente.PaneControl(
        searchDepth=1, ClassName="ToolbarWndClass"
        )
       

        tool_barra_cuenta = barra_vuenta_corriente.ToolBarControl(
            searchDepth=1, ClassName="ToolbarWindow32"
        )
        

        boton_buscar_cuenta = tool_barra_cuenta.ButtonControl(
            searchDepth=1, Name="Buscar Cuenta Corriente"
        )
        assert boton_buscar_cuenta.GetInvokePattern().Invoke()
        print(f"clic en {boton_buscar_cuenta}")

        sleep(10)

        ventana_busca_cuenta = self.ventana_cuenta_corriente.PaneControl(
            searchDepth=1, ClassName="SSTabCtlWndClass"
        )
        

        cuadro_cuenta = ventana_busca_cuenta.EditControl(
            searchDepth=1, Name="Estado de Cta. Cte."
        )
        cuadro_cuenta.SetFocus()
        cuadro_cuenta.GetValuePattern().SetValue(codigo_filter)

        cuadro_tickets = ventana_busca_cuenta.EditControl(searchDepth=1, AutomationId="23")
        cuadro_tickets.GetValuePattern().SetValue(razon_social)

        assert boton_buscar_cuenta.GetInvokePattern().Invoke()

        cuentas_corrientes_lista = ventana_busca_cuenta.PaneControl(
            searchDepth=1, ClassName="TL50.ApexList32.20"
        )
        

        barra_desplazable = cuentas_corrientes_lista.ScrollBarControl(
            searchDepth=1, AutomationId="52506"
        )
        rv = barra_desplazable.GetRangeValuePattern()

        todas_las_cuentas = {}

        if rv:
            print(f"Scroll actual: {rv.Value}, max: {rv.Maximum}")

            rect = cuentas_corrientes_lista.BoundingRectangle
            cuentas, _ = ocr_todo(rect, save_path="captura_panel_0.png")
            todas_las_cuentas.update(cuentas)

            for i in range(6):
                rv.SetValue(rv.Maximum)
                print(f"Intento {i+1}: Scroll movido al final")
                sleep(0.3)

                rect = cuentas_corrientes_lista.BoundingRectangle
                cuentas, _ = ocr_todo(rect, save_path=f"captura_panel_{i+1}.png")
                todas_las_cuentas.update(cuentas)

        else:
            print("La barra no soporta RangeValuePattern")
        rect = cuentas_corrientes_lista.BoundingRectangle
        

        cuentas, ultimo_codigo = ocr_todo(rect)

        if todas_las_cuentas:
            print("\n=== CUENTAS CORRIENTES DETECTADAS (CORREGIDAS) ===")
            for codigo in sorted(todas_las_cuentas):
                print(f"{codigo} → {todas_las_cuentas[codigo]}")
            print("===============================================")

            ultimo_codigo = list(sorted(todas_las_cuentas))[-1]

            print("\n=== ÚLTIMO CÓDIGO DETECTADO ===")
            print(f"{ultimo_codigo} → {todas_las_cuentas[ultimo_codigo]}")
            print("================================")
        else:
            print("No se detectaron cuentas")
            ultimo_codigo = None

        menu_bar = window.MenuBarControl(searchDepth=1, AutomationId="MenuBar")
        cerrar_cuenta = menu_bar.ButtonControl(searchDepth=1, Name="Cerrar")
        cerrar_cuenta.DoubleClick()
        
        self.ventana_cuenta_corriente.GetWindowPattern().Close()
        return {"todos": todas_las_cuentas, "ultimo": ultimo_codigo}
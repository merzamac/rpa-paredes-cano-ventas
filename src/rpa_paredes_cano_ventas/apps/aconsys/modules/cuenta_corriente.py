from uiautomation import WindowControl,PaneControl,ButtonControl,ToolBarControl,SendKeys,Click
from time import sleep
#from contabot_ventas.aconsys.ocr_utils import  ocr_todo

class CuentaCorriente:
    def __init__(self, ventana_cuenta_corriente: WindowControl):
        self.ventana_cuenta_corriente: WindowControl = ventana_cuenta_corriente
    @property
    def _buttons_area(self)-> ToolBarControl:
        toolbar_area = self.ventana_cuenta_corriente.PaneControl(searchDepth=1,ClassName="ToolbarWndClass")
        assert toolbar_area.Exists(maxSearchSeconds=15) 
        return toolbar_area.ToolBarControl(searchDepth=1,ClassName="ToolbarWindow32")

    @property
    def _form_area(self) -> PaneControl:
        form_area = self.ventana_cuenta_corriente.PaneControl(searchDepth=1, ClassName="SSTabCtlWndClass")
        assert form_area.Exists(maxSearchSeconds=15)
        return form_area
    @property
    def clients(self) -> None:
        check_clients = self._form_area.CheckBoxControl(searchDepth=1,AutomationId="13")
        toggle_state = check_clients.GetTogglePattern().ToggleState
        if (toggle_state != 1):
            check_clients.GetTogglePattern().SetToggleState(toggleState=1)
    @property
    def content(self):
        return self._form_area.PaneControl(searchDepth=1,ClassName="TL50.ApexList32.20")
    @property
    def provider(self)->None:
        check_provider = self._form_area.CheckBoxControl(searchDepth=1,AutomationId="12")
        toggle_state = check_provider.GetTogglePattern().ToggleState
        if (toggle_state != 1):
            check_provider.GetTogglePattern().SetToggleState(toggleState=1)
    def account_code(self, code:str)->None:
        edit_code = self._form_area.EditControl(searchDepth=1,AutomationId="22")
        assert edit_code.Exists(maxSearchSeconds=15)
        edit_code.GetValuePattern().SetValue(code)
    def ruc(self, ruc:str ="")->None:
        edit_ruc = self._form_area.EditControl(searchDepth=1,AutomationId="24")
        assert edit_ruc.Exists(maxSearchSeconds=15)
        edit_ruc.GetValuePattern().SetValue(ruc)
    def description(self, name:str)->None:
        edit_description = self._form_area.EditControl(searchDepth=1,AutomationId="23")
        assert edit_description.Exists(maxSearchSeconds=15)
        edit_description.GetValuePattern().SetValue(name)
    def document_type(self, a_type:str)->None:
        edit_control = self._form_area.PaneControl(searchDepth=1,AutomationId="3", foundIndex=2).EditControl(searchDepth=1, AutomationId="60666")
        assert edit_control.Exists(maxSearchSeconds=15)
        edit_control.Click(simulateMove=False)
        edit_control.SendKeys(a_type)
        SendKeys("{ENTER}")
        sleep(0.5)
        # lo tratamos como un EditControl aunque sea DocumentControl
        value = edit_control.GetValuePattern().Value.strip()
        if value != a_type:
            ValueError("No se logro hacer la eleccion correcta en el tipo de documento")
    @property
    def scroll_until_end(self)->None:
        sleep(0.5)
        content_area = self._form_area.PaneControl(searchDepth=1,ClassName="TL50.ApexList32.20")
        scroll_bar = content_area.ScrollBarControl(searchDepth=1, AutomationId="52506")
        left_button= content_area.ScrollBarControl(searchDepth=1, AutomationId="52505").ButtonControl(searchDepth=1,Name="Columna a la izquierda")
        page_down = scroll_bar.ButtonControl(searchDepth=1,Name="Av Pág")
        down_button = scroll_bar.ButtonControl(searchDepth=1,Name="Línea abajo")
        up_button = scroll_bar.ButtonControl(searchDepth=1,Name="Línea arriba")

        # coordenadas para ordenar numeros de cuentas corrientes
        x = left_button.BoundingRectangle.right
        y = up_button.BoundingRectangle.top

        Click(x=x, y=y)
        sleep(0.3)
        Click(x=x, y=y)

        assert page_down.Exists(maxSearchSeconds=15)
        assert down_button.Exists(maxSearchSeconds=15)
        # Usar Av Pág primero para scroll rápido
        click_count = 0
    
        while True:
            rect = page_down.BoundingRectangle
            if (rect.width() == 0 and rect.height() == 0):
                print(f"Línea abajo ya no visible después de {click_count} clicks")
                break
            
            page_down.Click()
            click_count += 1
            sleep(0.2)
            if click_count == 15:
                raise ValueError("Somethings wrong while trying to do scrolling")
        down_button.Click()
            
    @property
    def close(self)->None:
        self.ventana_cuenta_corriente.GetWindowPattern().Close()

        
    @property
    def start(self) -> None:
        start_button =self._buttons_area.ButtonControl(searchDepth=1,Name="Inicializar busqueda")
        assert start_button.Exists(maxSearchSeconds=15)
        start_button.GetInvokePattern().Invoke(waitTime=10)
    @property
    def search(self) -> None:
        search_button =self._buttons_area.ButtonControl(searchDepth=1,Name="Buscar Cuenta Corriente")
        assert search_button.Exists(maxSearchSeconds=15)
        search_button.GetInvokePattern().Invoke(waitTime=10)
    @property
    def save(self) ->None:
        save_button =self._buttons_area.ButtonControl(searchDepth=1,Name="Grabar Cuenta Corriente")
        assert save_button.Exists(maxSearchSeconds=15)
        save_button.GetInvokePattern().Invoke(waitTime=10)
    @property
    def new_account(self) ->None:
        new_button =self._buttons_area.ButtonControl(searchDepth=1,Name="Nueva Cuenta Corriente")
        assert new_button.Exists(maxSearchSeconds=15)
        new_button.GetInvokePattern().Invoke(waitTime=10)

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
            cuentas, _ = (0,0)#ocr_todo(rect, save_path="captura_panel_0.png")
            todas_las_cuentas.update(cuentas)

            for i in range(6):
                rv.SetValue(rv.Maximum)
                print(f"Intento {i+1}: Scroll movido al final")
                sleep(0.3)

                rect = cuentas_corrientes_lista.BoundingRectangle
                cuentas, _ = (0,0)#ocr_todo(rect, save_path=f"captura_panel_{i+1}.png")
                todas_las_cuentas.update(cuentas)
        else:
            print("La barra no soporta RangeValuePattern")
        rect = cuentas_corrientes_lista.BoundingRectangle
        

        cuentas, ultimo_codigo = ()#ocr_todo(rect)

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
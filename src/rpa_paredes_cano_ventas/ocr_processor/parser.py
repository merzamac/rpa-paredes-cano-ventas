
class DataParser:
    @staticmethod
    def clean_text(raw_text: str):
        # Convertimos el texto en una lista de líneas limpias
        lines = [line.strip() for line in raw_text.split('\n') if line.strip()]
        
        accounts = []
        companies = []

        for line in lines:
            # Regla 1: Si tiene exactamente 11 dígitos, es una cuenta
            if line.isdigit() and len(line) == 11:
                accounts.append(line)
                continue # Pasamos a la siguiente línea

            # Regla 2: Filtro para empresas
            # - Más de 5 caracteres
            # - No empieza por '0' (evita confusiones con cuentas mal leídas)
            # - No contiene la palabra 'TICKET'
            # - No es un encabezado conocido (C.C, LLI, RS, R)
            if len(line) >= 5:
                # Normalizamos a mayúsculas para comparar
                upper_line = line.upper()
                
                if (not upper_line.startswith('0') and 
                    'TICKET' not in upper_line and 
                    upper_line not in ['TICKETS', 'VARIOS', 'TICKETSYARIOS']):
                    
                    # Limpiamos el guion inicial si existe
                    clean_company = line.lstrip('-').strip()
                    companies.append(clean_company)


        if len(companies) != len(accounts):
            raise ValueError(f"⚠️ Atención: Se encontraron {len(accounts)} cuentas y {len(companies)} empresas.")
            

            
        return tuple(accounts), tuple(companies)

    @staticmethod
    def format_results(accounts: tuple, companies: tuple):
        # Combinamos ambos resultados en una lista de diccionarios
        # Usamos zip para emparejar cuenta con sucursal
        results = []
        for acc, desc in zip(accounts, companies):
            results.append({
                "cuenta_corriente": acc,
                "descripcion": f"TICKETS VARIOS - {desc}"
            })
        return results

        
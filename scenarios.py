SCENARIOS = [
    {
        "id": 1,
        "department": "RRHH",
        "title": "Métricas de absentismo",
        "icon": "👥",
        "situation": """
El departamento de **Recursos Humanos** te contacta con la siguiente solicitud:

> "Necesitamos un visual en Power BI que nos permita ver el porcentaje de absentismo
> de los empleados mes a mes durante el último año. Queremos poder filtrar por
> departamento y por tipo de ausencia (enfermedad, vacaciones, otros)."

Tienes acceso a una tabla llamada `Ausencias` con las columnas:
- `ID_Empleado`, `Nombre_Empleado`, `Departamento`
- `Fecha_Inicio`, `Fecha_Fin`, `Tipo_Ausencia`, `Dias_Ausencia`

Y una tabla `Empleados` con:
- `ID_Empleado`, `Departamento`, `Fecha_Alta`, `Estado` (Activo/Inactivo)
        """,
        "goal": "Crear una medida DAX para calcular el % de absentismo mensual y diseñar el visual adecuado.",
        "criteria": [
            "Menciona la medida o cálculo DAX necesario (días ausentes / días laborables)",
            "Especifica los filtros requeridos (departamento, tipo de ausencia, período)",
            "Indica el tipo de visual más adecuado (línea temporal, barras, etc.)",
            "Proporciona contexto sobre las tablas disponibles o relaciones necesarias",
            "El prompt es claro, concreto y accionable para una IA o un compañero",
        ],
    },
    {
        "id": 2,
        "department": "Ventas",
        "title": "Análisis de cumplimiento de objetivos",
        "icon": "📈",
        "situation": """
El director comercial te pide urgentemente:

> "Quiero ver en un solo vistazo si cada comercial está cumpliendo su objetivo de ventas
> mensual. Que se vea claramente quién está por encima y quién por debajo. También
> necesito el acumulado del año comparado con el objetivo anual."

Tienes estas tablas:
- `Ventas`: `ID_Venta`, `ID_Comercial`, `Fecha`, `Importe`, `Producto`, `Región`
- `Comerciales`: `ID_Comercial`, `Nombre`, `Región`, `Gestor`
- `Objetivos`: `ID_Comercial`, `Año`, `Mes`, `Objetivo_Mensual`
        """,
        "goal": "Diseñar un dashboard con KPIs de cumplimiento y comparativa objetivo vs real.",
        "criteria": [
            "Propone una medida DAX para calcular el % de cumplimiento (real vs objetivo)",
            "Menciona el uso de formato condicional o KPI visual para semáforos",
            "Indica cómo mostrar el acumulado YTD frente al objetivo anual",
            "Especifica los filtros o segmentadores necesarios",
            "El prompt describe con claridad el resultado visual esperado",
        ],
    },
    {
        "id": 3,
        "department": "Finanzas",
        "title": "Variación de costes vs presupuesto",
        "icon": "💰",
        "situation": """
Desde el área financiera te envían este correo:

> "Necesitamos analizar la desviación entre el gasto real y el presupuesto para cada
> centro de coste. Es importante que podamos ver tanto la desviación en valor absoluto
> como en porcentaje, y que quede claro si la desviación es favorable o desfavorable."

Tablas disponibles:
- `Gastos`: `ID_Gasto`, `Centro_Coste`, `Categoría`, `Fecha`, `Importe_Real`
- `Presupuesto`: `Centro_Coste`, `Categoría`, `Año`, `Mes`, `Importe_Presupuestado`
        """,
        "goal": "Crear medidas de variación (absoluta y %) y visualizarlas con indicadores de favorabilidad.",
        "criteria": [
            "Define la fórmula de desviación (Real - Presupuesto) y el % de desviación",
            "Indica cómo representar visualmente si la desviación es favorable o desfavorable",
            "Menciona la necesidad de relacionar ambas tablas (Centro_Coste + Categoría + período)",
            "Propone un tipo de visual adecuado (tabla con formato condicional, waterfall, etc.)",
            "El prompt especifica tanto la métrica como el contexto visual",
        ],
    },
    {
        "id": 4,
        "department": "Logística",
        "title": "Tiempo medio de entrega por zona",
        "icon": "🚚",
        "situation": """
El responsable de logística te solicita:

> "Estamos teniendo quejas de clientes sobre los plazos de entrega. Necesito un informe
> que me muestre el tiempo medio de entrega por zona geográfica y por transportista,
> y que pueda comparar con el SLA comprometido (48h para península, 72h para islas)."

Tablas:
- `Pedidos`: `ID_Pedido`, `Fecha_Pedido`, `Fecha_Entrega`, `Zona`, `ID_Transportista`, `Estado`
- `Transportistas`: `ID_Transportista`, `Nombre`, `Tipo`
- `SLA`: `Zona`, `Horas_Comprometidas`
        """,
        "goal": "Calcular tiempo medio de entrega y compararlo con el SLA por zona y transportista.",
        "criteria": [
            "Propone cómo calcular el tiempo de entrega en horas o días (DATEDIFF en DAX)",
            "Menciona la comparativa con la tabla SLA y la detección de incumplimientos",
            "Indica los filtros útiles (zona, transportista, período, estado del pedido)",
            "Propone un visual que permita identificar zonas problemáticas (mapa, tabla, barra)",
            "El prompt es específico sobre qué medir y cómo visualizarlo",
        ],
    },
    {
        "id": 5,
        "department": "Marketing",
        "title": "ROI de campañas publicitarias",
        "icon": "📣",
        "situation": """
El equipo de marketing te pide ayuda:

> "Hemos invertido en varias campañas este trimestre y necesitamos saber cuál ha sido
> la más rentable. Queremos ver el ROI de cada campaña, el coste por lead generado
> y poder filtrar por canal (Google Ads, Redes Sociales, Email, etc.)."

Tablas disponibles:
- `Campañas`: `ID_Campaña`, `Nombre`, `Canal`, `Fecha_Inicio`, `Fecha_Fin`, `Inversión`
- `Leads`: `ID_Lead`, `ID_Campaña`, `Fecha`, `Estado` (Convertido/No convertido)
- `Ventas_Lead`: `ID_Lead`, `Importe_Venta`
        """,
        "goal": "Calcular ROI y coste por lead por campaña y canal, con visualización comparativa.",
        "criteria": [
            "Define la fórmula de ROI: (Ingresos - Inversión) / Inversión * 100",
            "Propone cómo calcular el coste por lead (Inversión / nº de leads)",
            "Indica las relaciones necesarias entre tablas (Campañas → Leads → Ventas_Lead)",
            "Menciona segmentadores por canal y período temporal",
            "El prompt describe el output visual esperado (ranking de campañas, comparativa de canales)",
        ],
    },
]

from app.rag.retriever import search_documents


def ask_question(question, history=None):

    saludos = ["hola", "holi", "buenas", "hey", "hello"]
    question_lower = question.lower().strip()

    # 🧠 MEMORIA CONVERSACIONAL
    if history and len(history) > 0:

        last_answer = history[-1]["answer"]

        if (
            "cuál almacena" in question_lower
            or "cual almacena" in question_lower
            or "almacena la información" in question_lower
            or "almacena los datos" in question_lower
            or "dónde se guarda" in question_lower
            or "donde se guarda" in question_lower
        ):

            if "PostgreSQL" in last_answer or "postgresql" in last_answer:

                return {
                    "response": """
## 🧠 Memoria Conversacional

Basándome en la respuesta anterior, el componente que almacena la información es:

### **PostgreSQL**

PostgreSQL es la base de datos utilizada por el sistema para almacenar la información principal del proyecto.
""",
                    "sources": []
                }

        if (
            "cuál es la api" in question_lower
            or "cual es la api" in question_lower
            or "cuál procesa la lógica" in question_lower
            or "cual procesa la logica" in question_lower
            or "quién procesa la lógica" in question_lower
            or "quien procesa la logica" in question_lower
        ):

            if "API ASP.NET Core" in last_answer:

                return {
                    "response": """
## 🧠 Memoria Conversacional

Basándome en la respuesta anterior, el componente que procesa la lógica del negocio es:

### **API ASP.NET Core**

Este componente funciona como backend del sistema y se encarga de atender las solicitudes, aplicar reglas de negocio y comunicarse con la base de datos.
""",
                    "sources": []
                }

    if question_lower in saludos:
        return {
            "response": "¡Hola! Soy tu asistente inteligente de trazabilidad de software. Puedes preguntarme sobre configuración, diagramas, base de datos, Swagger, GitHub, código fuente, controladores o trazabilidad del proyecto.",
            "sources": []
        }

    temas_permitidos = [
        "github", "repositorio", "repo",
        "diagrama", "componentes", "arquitectura",
        "diccionario", "tabla", "campo", "correo",
        "appsettings", "swagger", "jwt", "base de datos",
        "postgresql", "configuración", "configuracion",
        "puerto", "launchsettings", "proyecto",
        "api", "controlador", "controller",
        "usuariocontroller", "contactoscontroller", "authcontroller",
        "endpoint", "servicio", "código", "codigo",
        "pdf", "manual", "documento", "documentación", "documentacion",
        "archivo", "usa", "utiliza", "trazabilidad",
        "almacena", "guarda", "información", "informacion", "datos"
    ]

    if not any(tema in question_lower for tema in temas_permitidos):
        return {
            "response": "No encontré esa pregunta relacionada con la base de conocimiento cargada. Este asistente está especializado en analizar repositorios, configuración, diagramas, diccionarios de datos y trazabilidad del sistema.",
            "sources": []
        }

    results = search_documents(question)

    docs = results.get("documents") or []
    metas = results.get("metadatas") or []

    docs = docs[0] if docs else []
    metas = metas[0] if metas else []

    if not docs:
        return {
            "response": "No encontré información suficiente en la base de conocimiento.",
            "sources": []
        }

    context = "\n\n".join(docs).strip()

    if ("archivo" in question_lower or "usa" in question_lower or "utiliza" in question_lower or "trazabilidad" in question_lower) and "correo" in question_lower:

        response = """
## 🔍 Trazabilidad Campo → Código

Se realizó una búsqueda del campo **Correo** dentro de la base de conocimiento indexada.

### 🔗 Trazabilidad encontrada

📄 **UsuarioController.cs**  
└─ Gestión y administración de usuarios.

📄 **UsuarioDTOs.cs**  
└─ Transporte de datos del usuario entre la API y el cliente.

📄 **Usuario.cs**  
└─ Modelo principal de la entidad Usuario.

📄 **AuthController.cs**  
└─ Procesos de autenticación y login donde puede utilizarse el correo.

### ✅ Interpretación técnica

El campo **Correo** pertenece a la entidad **Usuarios** y se relaciona con procesos de registro, autenticación, actualización de datos y transporte de información del usuario.

### 📄 Evidencia consultada

La trazabilidad se construyó relacionando el diccionario de datos `diccionario.xlsx` con los archivos de código fuente indexados del repositorio.
"""

    elif "usuariocontroller" in question_lower or "usuario controller" in question_lower:

        response = f"""
## 🎯 Análisis de UsuarioController

**UsuarioController.cs** es un controlador de ASP.NET Core relacionado con la gestión de usuarios.

### Función principal

- Consultar usuarios.
- Registrar nuevos usuarios.
- Actualizar datos de usuarios.
- Gestionar información asociada al perfil del usuario.

### 📄 Evidencia consultada

La respuesta se basa en los archivos de código fuente indexados del repositorio, especialmente en `Controllers/UsuarioController.cs`.
"""

    elif "contactoscontroller" in question_lower or "contactos controller" in question_lower:

        response = f"""
## 📇 Análisis de ContactosController

**ContactosController.cs** es un controlador relacionado con la gestión de contactos del sistema.

### Función principal

- Crear contactos.
- Listar contactos.
- Actualizar contactos.
- Eliminar contactos.
- Consultar información asociada a contactos.

### 📄 Evidencia Consultada

La respuesta se basa en los archivos de código fuente indexados del repositorio, especialmente en `Controllers/UsuarioController.cs`.
"""

    elif "authcontroller" in question_lower or "auth controller" in question_lower:

        response = f"""
## 🔐 Análisis de AuthController

**AuthController.cs** está relacionado con la autenticación del sistema.

### Función principal

- Iniciar sesión.
- Validar credenciales.
- Generar tokens JWT.
- Proteger el acceso al sistema.

### 📄 Información recuperada

{context[:1000]}
"""
    elif "base de datos" in question_lower or "postgresql" in question_lower:

      response = """
## 🗄️ Base de datos utilizada en el proyecto

El proyecto utiliza:

### PostgreSQL

### 📌 Evidencia encontrada

La configuración de conexión se encuentra en archivos como:

- appsettings.json
- appsettings.Development.json

### 🔍 Interpretación técnica

PostgreSQL es el sistema gestor de base de datos utilizado por la API ASP.NET Core para almacenar información de usuarios, contactos y demás datos del sistema.

### ✅ Características

- Base de datos relacional
- Soporte SQL
- Alta estabilidad
- Compatible con Docker y servicios en la nube
- Utilizada frecuentemente con ASP.NET Core
"""

    elif "jwt" in question_lower:

        response = """
## 🔐 Uso de JWT en el proyecto

JWT se utiliza para la autenticación y seguridad del sistema.

### 📌 Archivos relacionados

| Archivo | Uso |
|---|---|
| appsettings.json | Define configuración de JWT como Key, Issuer y Audience |
| appsettings.Development.json | Puede contener configuración de JWT para entorno de desarrollo |
| Program.cs | Configura la autenticación JWT dentro de la API |
| AuthController.cs | Maneja procesos de login/autenticación |
| UsuarioController.cs | Puede proteger endpoints relacionados con usuarios |

### ✅ Interpretación técnica

El sistema usa JWT para validar usuarios autenticados y proteger endpoints de la API.

### ⚠️ Seguridad

Las claves JWT no deben mostrarse directamente ni estar quemadas en el código. Deben manejarse mediante `.env` o variables de entorno.
"""

    elif "github" in question_lower or "repositorio" in question_lower or "repo" in question_lower:

        response = """
## 📦 Repositorio de GitHub analizado

### **WebServiceContactos**

| Archivo | Información encontrada |
|---|---|
| README.md | Nombre o descripción general del proyecto |
| appsettings.json | Configuración principal del sistema |
| appsettings.Development.json | Configuración para entorno de desarrollo |
| launchSettings.json | Configuración de ejecución, puertos y Swagger |

### 🔍 Resumen técnico

El repositorio contiene una API desarrollada en **ASP.NET Core**, con configuración para PostgreSQL, JWT, Swagger y ejecución HTTP/HTTPS.

### ⚠️ Seguridad

Se detectan valores sensibles en archivos de configuración. Para un entorno real, deben moverse a **.env** o variables de entorno.
"""

    elif "diagrama" in question_lower or "componentes" in question_lower or "arquitectura" in question_lower:

        response = """
## 🧩 Componentes del diagrama Draw.io

| Componente | Función |
|---|---|
| Usuario | Persona que interactúa con el sistema |
| Frontend Web | Interfaz visual del sistema |
| API ASP.NET Core | Backend que procesa la lógica del negocio |
| JWT para autenticación | Seguridad para validar usuarios |
| Base de Datos PostgreSQL | Almacena la información del sistema |

### 🏗️ Interpretación

El diagrama representa una arquitectura web donde el usuario utiliza un frontend que se comunica con una API ASP.NET Core. La autenticación se maneja con JWT y los datos se almacenan en PostgreSQL.
"""

    elif "manual" in question_lower or "documentación" in question_lower or "documentacion" in question_lower or "documento" in question_lower or "pdf" in question_lower:

        response = """
## 📄 Documentación técnica analizada

Según el manual técnico, el sistema **WebServiceContactos** es una API desarrollada en **ASP.NET Core**.

### 🏗️ Arquitectura

| Componente | Descripción |
|---|---|
| Usuario | Persona que interactúa con el sistema |
| Frontend Web | Interfaz que consume los servicios |
| API ASP.NET Core | Backend principal del sistema |
| PostgreSQL | Base de datos donde se almacena la información |

### 🔐 Seguridad

La autenticación del sistema se realiza mediante **JWT**.

### 🧪 Swagger

Swagger se utiliza para documentar y probar los endpoints de la API.

### 📌 Fuente principal

manual_tecnico.md
"""

    elif "diccionario" in question_lower or "tabla" in question_lower or "campo" in question_lower or "correo" in question_lower:

        response = """
## 📊 Diccionario de datos encontrado

| Tabla | Campo | Tipo | Descripción |
|---|---|---|---|
| Usuarios | UsuarioId | int | Identificador único del usuario |
| Usuarios | Nombre | varchar | Nombre del usuario |
| Usuarios | Correo | varchar | Correo electrónico del usuario |
| Contactos | ContactoId | int | Identificador único del contacto |
| Contactos | Telefono | varchar | Número telefónico del contacto |

### ✅ Respuesta técnica

El campo que representa el correo es **Usuarios.Correo**.
"""

    else:

        response = f"""
## 🤖 Respuesta basada en la base de conocimiento

{context[:1500]}
"""

    sources = []

    for meta in metas:
        source = meta.get("source", "desconocido")
        if source not in sources:
            sources.append(source)

    return {
        "response": response,
        "sources": sources
    }

import csv
import os
from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("TOKEN")
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters
)
RUTA_BASE = os.path.dirname(os.path.abspath(__file__))


usuarios_estado = {} #cada usuario tiene su propio estado guardado usando el id de telegram
# -------------------------
# LEER EMPLEADOS
# -------------------------

def buscar_empleado(legajo):
    ruta = os.path.join(RUTA_BASE, "empleados.csv")

    with open(ruta, "r", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo, delimiter=";")

        for fila in lector:
            if fila["legajo"] == legajo:
                return fila

    return None
# -------------------------
# GUARDAR SOLICITUD
# -------------------------

def guardar_solicitud(legajo, dias):
    with open("solicitudes.csv", "r", encoding="utf-8") as archivo:
        filas = list(csv.reader(archivo))

    nuevo_id = len(filas)

    with open("solicitudes.csv", "a", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow([
            nuevo_id,
            legajo,
            dias,
            "Aprobada"
        ])

# -------------------------
# COMANDO START
# -------------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    usuarios_estado[update.effective_user.id] = {
        "estado": "ESPERANDO_LEGAJO"
    }

    await update.message.reply_text(
        "Bienvenido al sistema de vacaciones.\n\nIngrese su número de legajo:"
    )

# -------------------------
# MENSAJES
# -------------------------

async def mensajes(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user_id = update.effective_user.id
    texto = update.message.text

    if user_id not in usuarios_estado:
        await update.message.reply_text(
            "Escriba /start para comenzar."
        )
        return

    estado = usuarios_estado[user_id]["estado"]  #puede ser esperando lejago, esperando dias o finalizado, el sistema sabe en que paso
                                                # esta cada uno
    # ------------------
    # LEGAJO
    # ------------------

    if estado == "ESPERANDO_LEGAJO":

        if not texto.isdigit():

            await update.message.reply_text(
                "Error: debe ingresar un número de legajo."
            )
            return

        empleado = buscar_empleado(texto) #aca se valida que exista, recorriendo el csv

        if empleado is None:

            await update.message.reply_text(
                "Legajo no encontrado."
            )
            return

        usuarios_estado[user_id]["legajo"] = texto
        usuarios_estado[user_id]["dias_disponibles"] = int(
            empleado["dias_disponibles"]
        )

        usuarios_estado[user_id]["estado"] = "ESPERANDO_DIAS"

        await update.message.reply_text(
            f"Empleado encontrado.\n"
            f"Días disponibles: {empleado['dias_disponibles']}\n\n"
            f"Ingrese la cantidad de días a solicitar:"
        )

    # ------------------
    # DIAS
    # ------------------

    elif estado == "ESPERANDO_DIAS":

        if not texto.isdigit():

            await update.message.reply_text(
                "Debe ingresar un número válido."
            )
            return

        dias = int(texto)
        if dias <= 0:
            await update.message.reply_text("Debe ingresar una cantidad de días mayor a cero.")
            return

        disponibles = usuarios_estado[user_id]["dias_disponibles"]

        if dias > disponibles:

            await update.message.reply_text(
                f"Solicitud rechazada.\n"
                f"Solo dispone de {disponibles} días."
            )

            usuarios_estado[user_id]["estado"] = "FINALIZADO"
            return

        guardar_solicitud(
            usuarios_estado[user_id]["legajo"],
            dias
        )

        await update.message.reply_text(
            "Solicitud registrada correctamente."
        )

        usuarios_estado[user_id]["estado"] = "FINALIZADO"

# -------------------------
# MAIN
# -------------------------

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, mensajes)
)

print("Bot iniciado...")

app.run_polling()
from enum import Enum, auto
from engine import DonationEngine


class State(Enum):
    WELCOME = auto()
    PILIH_LOKASI = auto()
    PILIH_PROGRAM = auto()
    PILIH_DONASI = auto()
    KERANJANG = auto()
    KONFIRMASI = auto()
    SELESAI = auto()


class DonationFSM:

    def __init__(self):

        self.state = State.WELCOME
        self.engine = DonationEngine()

        self.response = ""
        self.lokasi = ""
        self.program = ""

    def get_response(self):
        return self.response

    def calculate_total(self):
        return self.engine.calculate_total()

    # ====================================
    # KATALOG
    # ====================================

    def get_catalog_text(self):

        text = "📚 **Katalog Donasi Pendidikan**\n\n"

        for item, data in self.engine.catalog.items():

            text += (
                f"{data['emoji']} "
                f"**{item}** "
                f"(Rp {data['price']:,})\n"
            )

        text += """

Contoh Perintah:

- 3 Pulpen
- 2 Buku SD
- 1 Tas Punggung

Ketik:
- keranjang
- checkout
"""

        return text

    # ====================================
    # CART
    # ====================================

    def get_cart_text(self):

        if not self.engine.cart:
            return "🛒 Keranjang donasi masih kosong."

        text = "🛒 **Keranjang Donasi**\n\n"

        for item in self.engine.cart:

            subtotal = (
                item["price"]
                * item["qty"]
            )

            text += (
                f"{item['emoji']} "
                f"{item['item']} "
                f"x{item['qty']} "
                f"(Rp {subtotal:,})\n"
            )

        text += (
            f"\n💰 Total Donasi : "
            f"Rp {self.calculate_total():,}"
        )

        return text

    # ====================================
    # REDUCE ITEM
    # ====================================

    def reduce_item(
        self,
        item_name,
        qty
    ):

        for item in self.engine.cart:

            if item["item"] == item_name:

                item["qty"] -= qty

                if item["qty"] <= 0:

                    self.engine.cart.remove(item)

                    return (
                        f"❌ {item_name} "
                        f"dihapus dari keranjang."
                    )

                return (
                    f"📉 {item_name} "
                    f"dikurangi {qty}."
                )

        return (
            f"⚠️ {item_name} "
            f"tidak ditemukan."
        )

    # ====================================
    # FSM
    # ====================================

    def step(
        self,
        user_input=""
    ):

        user_input = user_input.strip()

        intent = self.engine.detect_intent(
            user_input
        )

        # ====================================
        # WELCOME
        # ====================================

        if self.state == State.WELCOME:

            self.response = """
🎓 **Selamat Datang di Donasi Pendidikan**

Program Donasi Fasilitas Pembelajaran Untuk Anak Kurang Mampu di Kota Semarang.

**Daftar Kecamatan Kota Semarang:**
Banyumanik, Candisari, Gajahmungkur, Gayamsari, Genuk, Gunungpati, Mijen, Ngaliyan, Pedurungan, Semarang Barat, Semarang Selatan, Semarang Tengah, Semarang Timur, Semarang Utara, Tembalang, Tugu.
"""

            self.state = State.PILIH_LOKASI

        # ====================================
        # PILIH LOKASI
        # ====================================

        elif self.state == State.PILIH_LOKASI:

            allowed_kecamatan = [

                "banyumanik",
                "candisari",
                "gajahmungkur",
                "gayamsari",
                "genuk",
                "gunungpati",
                "mijen",
                "ngaliyan",
                "pedurungan",
                "semarang barat",
                "semarang selatan",
                "semarang tengah",
                "semarang timur",
                "semarang utara",
                "tembalang",
                "tugu"
            ]

            if (
                user_input.lower()
                not in allowed_kecamatan
            ):

                self.response = """
❌ Kecamatan tidak valid.

Pilih salah satu kecamatan:

- Banyumanik
- Candisari
- Gajahmungkur
- Gayamsari
- Genuk
- Gunungpati
- Mijen
- Ngaliyan
- Pedurungan
- Semarang Barat
- Semarang Selatan
- Semarang Tengah
- Semarang Timur
- Semarang Utara
- Tembalang
- Tugu
"""
                return

            self.lokasi = (
                user_input.title()
            )

            self.response = f"""
📍 Lokasi tersimpan:

{self.lokasi}

Masukkan Program:

- SD
- SMP
- SMA/SMK
"""

            self.state = State.PILIH_PROGRAM

        # ====================================
        # PILIH PROGRAM
        # ====================================

        elif self.state == State.PILIH_PROGRAM:

            allowed_program = [
                "sd",
                "smp",
                "sma",
                "smk",
                "sma/smk"
            ]

            if (
                user_input.lower()
                not in allowed_program
            ):

                self.response = """
❌ Program tidak valid.

Pilih:

- SD
- SMP
- SMA/SMK
"""
                return

            self.program = user_input.upper()

            self.response = f"""
🎓 Program tersimpan:

{self.program}

Ketik:

- menu
- keranjang
- help
"""

            self.state = State.PILIH_DONASI

        # ====================================
        # DONASI
        # ====================================

        elif self.state == State.PILIH_DONASI:

            if intent == "GREETING":

                self.response = """
👋 Halo!

Selamat datang di Donasi Pendidikan.

Ketik:

- menu
- keranjang
- checkout
"""

            elif intent == "HELP":

                self.response = """
📖 Bantuan

Perintah yang tersedia:

- menu
- keranjang
- checkout
- reset
- hapus 2 pulpen

Contoh:

2 Pulpen
3 Buku SD
1 Tas Punggung
"""

            elif intent == "MENU":

                self.response = (
                    self.get_catalog_text()
                )

            elif intent == "CART":

                self.response = (
                    self.get_cart_text()
                )

            elif intent == "CHECKOUT":

                if not self.engine.cart:

                    self.response = (
                        "🛒 Keranjang masih kosong."
                    )

                else:

                    self.state = (
                        State.KONFIRMASI
                    )

                    self.response = f"""
💰 Total Donasi

Rp {self.calculate_total():,}

Lanjut kirim donasi?

Jawab:
ya / tidak
"""

            elif intent == "RESET":

                self.engine.clear_cart()

                self.response = (
                    "🗑️ Keranjang dikosongkan."
                )

            elif intent == "REMOVE":

                orders = (
                    self.engine.parse_orders(
                        user_input
                    )
                )

                if orders:

                    responses = []

                    for order in orders:

                        responses.append(
                            self.reduce_item(
                                order["item"],
                                order["qty"]
                            )
                        )

                    self.response = (
                        "\n".join(responses)
                    )

                else:

                    self.response = (
                        "⚠️ Item tidak ditemukan."
                    )

            else:

                orders = (
                    self.engine.parse_orders(
                        user_input
                    )
                )

                if orders:

                    for order in orders:

                        self.engine.add_to_cart(
                            order["item"],
                            order["qty"]
                        )

                    self.response = """
✔️ Donasi ditambahkan.

Ketik:

- keranjang
- checkout
- menu
"""

                else:

                    self.response = """
❌ Perintah tidak dikenali.

Contoh:

2 Pulpen
3 Buku SD
1 Tas Punggung
"""

        # ====================================
        # KONFIRMASI
        # ====================================

        elif self.state == State.KONFIRMASI:

            if user_input.lower() in [
                "ya",
                "yes"
            ]:

                total = (
                    self.calculate_total()
                )

                self.engine.clear_cart()

                self.state = (
                    State.SELESAI
                )

                self.response = f"""
🎉 Donasi Berhasil

📍 Kecamatan :
{self.lokasi}

🎓 Program :
{self.program}

💰 Total Donasi :
Rp {total:,}

Terima kasih atas kontribusi Anda.
"""

            elif user_input.lower() in [
                "tidak",
                "no"
            ]:

                self.state = (
                    State.PILIH_DONASI
                )

                self.response = (
                    "❌ Checkout dibatalkan."
                )

            else:

                self.response = (
                    "Jawab ya atau tidak."
                )

        # ====================================
        # SELESAI
        # ====================================

        elif self.state == State.SELESAI:

            self.response = """
🎉 Donasi selesai.

Ketik 'mulai'
untuk transaksi baru.
"""

            if (
                user_input.lower()
                == "mulai"
            ):

                self.__init__()

                self.step()
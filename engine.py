import re


class DonationEngine:

    def __init__(self):

        self.catalog = {

    # ==========================
    # BUKU AKADEMIK
    # ==========================

    "Buku SD": {
        "price": 50000,
        "emoji": "📚",
        "desc": "Buku Pembelajaran SD"
    },

    "Buku SMP": {
        "price": 60000,
        "emoji": "📖",
        "desc": "Buku Pembelajaran SMP"
    },

    "Buku SMA/SMK": {
        "price": 75000,
        "emoji": "📘",
        "desc": "Buku Pembelajaran SMA/SMK"
    },

    # ==========================
    # ALAT TULIS SISWA
    # ==========================

    "Pulpen": {
        "price": 5000,
        "emoji": "🖊️",
        "desc": "Pulpen siswa"
    },
    
    "Kotak Alat Tulis": {
    "price": 30000,
    "emoji": "🧰",
    "desc": "Kotak perlengkapan alat tulis"
    },
    
    "Pensil": {
        "price": 3000,
        "emoji": "✏️",
        "desc": "Pensil siswa"
    },
    
    "Penggaris": {
        "price": 4000,
        "emoji": "📏",
        "desc": "Penggaris siswa"
    },
    "Penghapus": {
        "price": 2000,
        "emoji": "🧽",
        "desc": "Penghapus pensil"
    },
    
    "Penghapus Pulpen": {
        "price": 7000,
        "emoji": "🖋️",
        "desc": "Correction Pen"
    },

    "Buku Tulis": {
        "price": 6000,
        "emoji": "📒",
        "desc": "Buku tulis siswa"
    },

    "Tas Punggung": {
        "price": 120000,
        "emoji": "🎒",
        "desc": "Tas sekolah"
    },

    # ==========================
    # ALAT PENGAJAR
    # ==========================

    "Papan Tulis": {
        "price": 350000,
        "emoji": "📋",
        "desc": "Papan tulis kelas"
    },

    "Spidol": {
        "price": 15000,
        "emoji": "🖍️",
        "desc": "Spidol pengajar"
    },

    "Penghapus Papan Tulis": {
        "price": 12000,
        "emoji": "🧹",
        "desc": "Penghapus papan tulis"
    },

    # ==========================
    # PENUNJANG PEMBELAJARAN
    # ==========================

    "Meja Siswa": {
        "price": 250000,
        "emoji": "🪑",
        "desc": "Meja belajar"
    },

    "Kursi Siswa": {
        "price": 150000,
        "emoji": "💺",
        "desc": "Kursi belajar"
    },

    # ==========================
    # OPERASIONAL
    # ==========================

    "Sewa Ruangan Belajar": {
        "price": 1000000,
        "emoji": "🏫",
        "desc": "Biaya sewa ruang pembelajaran"
    },

    "Upah Pengajar Sukarela": {
        "price": 500000,
        "emoji": "👨‍🏫",
        "desc": "Biaya operasional pengajar"
    },
    "Sewa Fasilitas Pelaksanaan Kegiatan": {
        "price": 750000,
        "emoji": "🏢",
        "desc": "Biaya sewa fasilitas untuk pelaksanaan kegiatan pendidikan"
    },

    # ==========================
    # BEASISWA
    # ==========================

    "Beasiswa Uang Saku": {
        "price": 500000,
        "emoji": "🎓",
        "desc": "Bantuan uang saku siswa"
    }
}
        self.cart = []

        self.re_number = r"\b(\d+)\b"

        item_names = sorted(
            [re.escape(item.lower()) for item in self.catalog.keys()],
            key=len,
            reverse=True
        )

        self.re_item = rf"({'|'.join(item_names)})"

        self.re_split = r"[,.]|\bdan\b|\b&\b"

    # ==========================
    # CART
    # ==========================

    def add_to_cart(self, item_name, qty=1):

        if item_name not in self.catalog:
            return

        for item in self.cart:

            if item["item"] == item_name:
                item["qty"] += qty
                return

        self.cart.append({
            "item": item_name,
            "qty": qty,
            "price": self.catalog[item_name]["price"],
            "emoji": self.catalog[item_name]["emoji"]
        })

    def clear_cart(self):
        self.cart.clear()

    def remove_item(self, item_name):

        self.cart = [
            item
            for item in self.cart
            if item["item"] != item_name
        ]

    # ==========================
    # TOTAL
    # ==========================

    def calculate_total(self):

        return sum(
            item["price"] * item["qty"]
            for item in self.cart
        )

    # ==========================
    # NLP PARSER
    # ==========================

    def parse_orders(self, text):

        text = text.lower()

        segments = re.split(
            self.re_split,
            text
        )

        results = []

        for segment in segments:

            item_match = re.search(
                self.re_item,
                segment
            )

            if not item_match:
                continue

            item_lower = item_match.group(1)

            real_name = None

            for key in self.catalog.keys():

                if key.lower() == item_lower:
                    real_name = key
                    break

            qty_match = re.search(
                self.re_number,
                segment
            )

            qty = (
                int(qty_match.group(1))
                if qty_match
                else 1
            )

            results.append({
                "item": real_name,
                "qty": qty
            })

        return results

    # ==========================
    # INTENT DETECTION
    # ==========================

    def detect_intent(self, text):

        text = text.lower().strip()

        # Salam
        if re.search(
            r"\b(halo|hai|hi|assalamualaikum)\b",
            text
        ):
            return "GREETING"

        # Bantuan
        if re.search(
            r"\b(help|bantuan|tolong)\b",
            text
        ):
            return "HELP"

        # Reset keranjang
        if re.search(
            r"\b(reset|ulang)\b",
            text
        ):
            return "RESET"

        # Lihat katalog
        if re.search(
            r"\b(menu|katalog|daftar)\b",
            text
        ):
            return "MENU"

        # Lihat keranjang
        if re.search(
            r"\b(keranjang|cart)\b",
            text
        ):
            return "CART"

        # Checkout
        if re.search(
            r"\b(kirim|checkout|bayar|selesai)\b",
            text
        ):
            return "CHECKOUT"

        # Hapus item
        if re.search(
            r"\b(hapus|batalkan)\b",
            text
        ):
            return "REMOVE"

        # Default
        return "ORDER"
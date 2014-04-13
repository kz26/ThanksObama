import sqlite3

class LCDInterface(object):
	def __init__(self):
		self.conn = sqlite3.connect('lcd.sqlite')

	def random_icd10(self):
		# return a random ICD10 code from the ICD10 supported procedures table
		qr = self.conn.execute("SELECT DISTINCT icd10 FROM icd10_support ORDER BY RANDOM() LIMIT 1")
		return qr.fetchone()[0]

	def random_procedure(self):
		# return a random procedure id, title from the LCD table
		qr = self.conn.execute("SELECT DISTINCT * FROM lcd ORDER BY RANDOM() LIMIT 1")
		return qr.fetchone()

	def get_icd10_procedures(self, icd10):
		# return supported procedures for a given ICD10
		qr = self.conn.execute("SELECT title FROM lcd WHERE lcd_id in (SELECT lcd_id FROM icd10_support WHERE icd10=?", (icd10,))
		return qr.fetchall()

	def get_icd10_unsupported_procedures(self, icd10):
		# return unsupported procedures for a given ICD10
		qr = self.conn.execute("SELECT title FROM lcd WHERE lcd_id in (SELECT lcd_id FROM icd10_nosupport WHERE icd10=?", (icd10,))
		return qr.fetchall()


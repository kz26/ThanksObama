import os
import sqlite3

class LCDInterface(object):
	def __init__(self):
		
		self.conn = sqlite3.connect(os.path.join(os.path.dirname(__file__), 'lcd.sqlite'), check_same_thread=False)
		self.conn.text_factory = lambda x: unicode(x, 'utf-8', 'ignore') # fix unicode issues

	def random_icd10(self):
		# return a random ICD10 code from the ICD10 supported procedures table
		qr = self.conn.execute("SELECT DISTINCT icd10 FROM icd10_support ORDER BY RANDOM() LIMIT 1")
		return qr.fetchone()[0]

	def random_procedure(self):
		# return a random procedure from the LCD table
		qr = self.conn.execute("SELECT DISTINCT title FROM lcd ORDER BY RANDOM() LIMIT 1")
		return qr.fetchone()[0]

	def random_supported_procedure(self):
		# return a random supported procedure that appears IN the icd10_support table
		qr = self.conn.execute("SELECT * FROM lcd WHERE lcd_id IN (SELECT DISTINCT lcd_id FROM icd10_support ORDER BY RANDOM() LIMIT 1)")
		return qr.fetchone()

	def get_icd10_procedures(self, icd10):
		# return supported procedures for a given ICD10
		qr = self.conn.execute("SELECT title FROM lcd WHERE lcd_id IN (SELECT lcd_id FROM icd10_support WHERE icd10=?)", (icd10,))
		return qr.fetchall()

	def get_icd10_unsupported_procedures(self, icd10):
		# return unsupported procedures for a given ICD10
		qr = self.conn.execute("SELECT title FROM lcd WHERE lcd_id IN (SELECT lcd_id FROM icd10_nosupport WHERE icd10=?)", (icd10,))
		return qr.fetchall()

	def get_procedure_supported_icd10s(self, lcd_id):
		# return supported ICD10s associated with a procedure ID
		qr = self.conn.execute("SELECT icd10 FROM icd10_support WHERE lcd_id=?", (lcd_id,))
		return qr.fetchall()

	def get_procedure_unsupported_icd10s(self, lcd_id):
		# return unsupported ICD10s associated with a procedure ID
		qr = self.conn.execute("SELECT icd10 FROM icd10_nosupport WHERE lcd_id=?", (lcd_id,))
		return qr.fetchall()

LCDInterface = LCDInterface()

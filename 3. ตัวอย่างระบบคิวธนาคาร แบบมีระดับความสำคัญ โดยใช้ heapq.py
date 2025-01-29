import heapq
from datetime import datetime
import time

class BankCustomer:
    def __init__(self, customer_id, service_type, is_premium=False):
        self.customer_id = customer_id  # ใช้ customer_id แทนชื่อ
        self.service_type = service_type
        self.is_premium = is_premium
        self.arrival_time = datetime.now()
        
        # กำหนดลำดับความสำคัญตาม service_type และสถานะลูกค้า
        self.priority = self._calculate_priority()
        
    def _calculate_priority(self):
        # ลำดับความสำคัญ (ยิ่งน้อยยิ่งสำคัญ)
        priority = {
            'ฝาก-ถอน': 3,
            'ชำระค่าบริการ': 2,
            'เปิดบัญชี': 1,
            'สินเชื่อ': 0
        }
        
        # ลูกค้า Premium จะได้ priority สูงกว่าปกติ 1 ระดับ
        base_priority = priority.get(self.service_type, 4)
        if self.is_premium:
            base_priority -= 0.5
            
        return base_priority
        
    def __lt__(self, other):
        # เปรียบเทียบลำดับความสำคัญ
        if self.priority == other.priority:
            # ถ้าความสำคัญเท่ากัน ใช้เวลามาก่อน-หลัง
            return self.arrival_time < other.arrival_time
        return self.priority < other.priority
        
class BankQueue:
    def __init__(self):
        self.queue = []  # heap queue
        self.waiting_count = 0
        self.current_id = 1  # เริ่มต้นที่หมายเลขคิวแรก
        
    def add_customer(self, customer):
        customer.customer_id = self.current_id  # กำหนดหมายเลขคิว
        self.current_id += 1
        heapq.heappush(self.queue, customer)
        self.waiting_count += 1
        print(f"เลขคิว: {customer.customer_id}")
        print(f"บริการ: {customer.service_type}")
        print(f"สถานะ: {'Premium' if customer.is_premium else 'ทั่วไป'}")
        print(f"จำนวนคิวรอ: {self.waiting_count}")
        print("-" * 30)
        
    def serve_next_customer(self):
        if not self.queue:
            print("ไม่มีลูกค้าในคิว")
            return None
            
        customer = heapq.heappop(self.queue)
        self.waiting_count -= 1
        
        wait_time = datetime.now() - customer.arrival_time
        print(f"\nเรียกลูกค้า เลขคิว: {customer.customer_id}")
        print(f"บริการ: {customer.service_type}")
        print(f"เวลารอ: {wait_time.seconds} วินาที")
        print(f"จำนวนคิวรอ: {self.waiting_count}")
        print("-" * 30)
        
        return customer
        
    def display_queue(self):
        if not self.queue:
            print("ไม่มีลูกค้าในคิว")
            return
            
        print("\nรายการคิวที่รอ:")
        # สร้าง copy ของคิวเพื่อไม่ให้กระทบคิวจริง
        temp_queue = self.queue.copy()
        position = 1
        
        while temp_queue:
            customer = heapq.heappop(temp_queue)
            print(f"{position}. เลขคิว: {customer.customer_id} - {customer.service_type}")
            position += 1
        print("-" * 30)

    def get_transaction_types(self):
        # แสดงรายการธุรกรรมให้ผู้ใช้เลือก
        print("\nเลือกธุรกรรมที่ต้องการทำ:")
        print("1. ฝาก-ถอน")
        print("2. ชำระค่าบริการ")
        print("3. เปิดบัญชี")
        print("4. สินเชื่อ")
        
        transaction_choice = input("กรุณาเลือกธุรกรรม (1-4): ")
        return transaction_choice


# ตัวอย่างการใช้งาน
def demo_bank_queue():
    bank = BankQueue()
    
    # เพิ่มลูกค้าเข้าคิว
    customers = [
        BankCustomer("C001", "ฝาก-ถอน"),
        BankCustomer("C002", "สินเชื่อ", is_premium=True),
        BankCustomer("C003", "ชำระค่าบริการ"),
        BankCustomer("C004", "เปิดบัญชี"),
        BankCustomer("C005", "สินเชื่อ")
    ]
    
    # จำลองให้ผู้ใช้เลือกธุรกรรม
    while True:
        # ผู้ใช้เลือกธุรกรรม
        transaction_choice = bank.get_transaction_types()
        
        if transaction_choice == "1":
            service_type = "ฝาก-ถอน"
        elif transaction_choice == "2":
            service_type = "ชำระค่าบริการ"
        elif transaction_choice == "3":
            service_type = "เปิดบัญชี"
        elif transaction_choice == "4":
            service_type = "สินเชื่อ"
        else:
            print("ตัวเลือกไม่ถูกต้อง! กรุณาเลือกใหม่.")
            continue
        
        # เพิ่มลูกค้าเข้าคิวตามบริการที่เลือก
        customer = BankCustomer(f"C{bank.current_id}", service_type)
        bank.add_customer(customer)
        
        # แสดงรายการคิว
        print("\nแสดงลำดับคิว:")
        bank.display_queue()
        
        # จำลองการเรียกลูกค้าเข้ารับบริการ
        serve_another = input("\nต้องการเรียกลูกค้าคิวถัดไปหรือไม่? (y/n): ")
        if serve_another.lower() == "y":
            bank.serve_next_customer()
        else:
            break
        
        time.sleep(1)

if __name__ == "__main__":
    demo_bank_queue()
    

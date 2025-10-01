const crypto = require("crypto");

// ==================
// Block structure
// ==================
class Block {
  constructor(index, data, prevHash = "0") {
    this.index = index;
    this.timestamp = Date.now();
    this.data = data;
    this.prevHash = prevHash;
    this.nonce = 0;
    this.hash = this.calcHash();
  }

  calcHash() {
    return crypto
      .createHash("sha256")
      .update(this.index + this.timestamp + this.data + this.prevHash + this.nonce)
      .digest("hex");
  }
}

// ==================
// Blockchain
// ==================
class Blockchain {
  constructor() {
    this.chain = [this.createGenesis()];
  }

  createGenesis() {
    return new Block(0, "Genesis Block", "0");
  }

  // إضافة بلوك جديد
  setBlock(data) {
    const prevBlock = this.chain[this.chain.length - 1];
    const newBlock = new Block(this.chain.length, data, prevBlock.hash);
    this.chain.push(newBlock);
  }

  // جلب بلوك برقم
  getBlock(index) {
    return this.chain[index] || null;
  }

  // استعراض كل البلوكات
  blocksExplorer() {
    this.chain.forEach((block) => {
      console.log("Index:", block.index);
      console.log("Timestamp:", block.timestamp);
      console.log("Data:", block.data);
      console.log("Prev Hash:", block.prevHash);
      console.log("Hash:", block.hash);
      console.log("Nonce:", block.nonce);
      console.log("-".repeat(40));
    });
  }

  // تعدين بلوك
  mineBlock(block, difficulty = 3) {
    const target = "0".repeat(difficulty);
    while (!block.hash.startsWith(target)) {
      block.nonce++;
      block.hash = block.calcHash();
    }
    console.log(`Block ${block.index} mined: ${block.hash}`);
  }
}

// ==================
// Test
// ==================
const bc = new Blockchain();

bc.setBlock("Transaction 1: Alice -> Bob");
bc.setBlock("Transaction 2: Bob -> Charlie");

// تعدين آخر بلوك
let lastBlock = bc.chain[bc.chain.length - 1];
bc.mineBlock(lastBlock, 3);

// استعراض البلوكات
bc.blocksExplorer();

// جلب بلوك محدد
const block1 = bc.getBlock(1);
console.log("\nBlock at index 1:", block1);

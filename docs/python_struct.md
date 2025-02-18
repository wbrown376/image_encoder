# Python 中的 struct 模块

在 Python 中，`struct` 模块提供了处理二进制数据的功能，其中 `struct.unpack` 函数用于将二进制数据解析为 Python 对象。这个函数的第一个参数是格式字符串，它决定了如何解析二进制数据。

格式字符串是由一个或多个格式字符组成的字符串，每个格式字符指定了二进制数据中的一个字段的类型和顺序。下面是 `struct` 模块中常用的格式字符：

### 格式字符

- `b`：signed byte（1个字节）
- `B`：unsigned byte（1个字节）
- `h`：short（2个字节）
- `H`：unsigned short（2个字节）
- `i`：int（4个字节）
- `I`：unsigned int（4个字节）
- `l`：long（4个字节）
- `L`：unsigned long（4个字节）
- `q`：long long（8个字节）
- `Q`：unsigned long long（8个字节）
- `f`：float（4个字节）
- `d`：double（8个字节）
- `s`：字符串（长度可变）
- `p`：*pascal string（长度可变，前一个字节指定长度）
- `x`：填充字节
- `P`：:void *（可变长度）

注意：
- 按照系统的字节序进行解析，这有两种：大端字节序（`>`) 和小端字节序（`<`)，它们分别使用大于号（>）和小于号（<）来指定。
- 可以使用 `@` 来指定系统的默认字节序。

### 示例

```python
import struct

# 一个示例二进制数据
data = b'\x01\x02\x03\x04\x05\x06\x07\x08'

# 使用大端字节序解析两个unsigned int
result = struct.unpack('>II', data)
print(result)

# 使用小端字节序解析两个unsigned int
result = struct.unpack('<II', data)
print(result)

# 解析一个 signed int 和一个 float
data2 = b'\x01\x00\x00\x00\x00\x00\x80\x3f'
result = struct.unpack('if', data2)
print(result)
```

### 字节序

在使用 `struct.unpack` 时，字节序的选择非常重要。字节序决定了多字节数据在内存中的存储顺序。大端字节序（big-endian）是将最高位字节存储在最低内存地址，小端字节序（little-endian）则相反。

- `>`：大端字节序
- `<`：小端字节序
- `=`：系统原生字节序
- `@`：与 `=` 相同，但更明确

在处理不同系统或设备之间的数据交换时，必须特别注意字节序的差异，以确保数据被正确解析。
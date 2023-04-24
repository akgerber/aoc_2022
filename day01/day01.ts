export {}

const filePath = Deno.args[0]
const lines = await Deno.readTextFile(filePath)

const split_lines = lines.split("\n\n")

const sums = split_lines.forEach((chunk) => {chunk.split("\n")})

console.log(split_lines)
console.log(sums)


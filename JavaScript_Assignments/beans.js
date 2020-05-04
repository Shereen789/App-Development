const countBs = function (ip_string) {
    let count = 0;
    let len = ip_string.length;
    for (let i = 0; i < len; i++) {
        if (ip_string[i] == "B") {
            count += 1
        }
    }
    return count
}

const countChar = function (ip_string, n) {
    let count = 0;
    let len = ip_string.length;
    for (let i = 0; i < len; i++) {
        if (ip_string[i] == n) {
            count += 1
        }
    }
    return count
}
ip_string = "Hello Busy People. Stay Home. Be safe. Be Happy"
console.log(countBs(ip_string))
console.log(countChar(ip_string, 'e'))

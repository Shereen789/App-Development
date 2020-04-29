const deepEqual = function (v1, v2) {
    if (v1 === v2) {
        return true
    }
    if (typeof v1 == "object" && typeof v2 == "object" && v1 != null && v2 != null) {
        if (Object.keys(v1).length == Object.keys(v2).length) {
            for (const key in v1) {
                if (!deepEqual(v1[key], v2[key])) {
                    return false
                }

            }
            return true
        }
    }
    return false
}

const v1 = {
    place: "Kurnool",
    state: "AndhraPradesh",
    country: "India"
}
const v2 = {
    place: "Tirupati",
    state: "AndhraPradesh",
    country: "India"
}
console.log(deepEqual(v1, v2))
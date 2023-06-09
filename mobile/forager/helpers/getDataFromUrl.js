export function getAccesToken(url) {
    const access_token = url.match(/access_token=[.A-Za-z0-9_-]*/g)[0]
    return access_token.split("=")[1]
}

export function getQueryParams(url) {
    const matches = url.match(/[.A-Za-z0-9_-]*=[.A-Za-z0-9_-]*/g)
    let params = {}

    for (let match of matches ) {
        const [param, value] = match.split("=")
        const paramObject = {[param]: value}
        params = Object.assign(params, paramObject)
    }

    return params
}
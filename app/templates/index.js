const getImage = async (url) => {
    const response = await fetch(url)
    const data = await response.blob()
    return data
}

// getImage("http://localhost:5000/api/questions_a/the_deadliest_attack_types").then(res => {
//     const img = URL.createObjectURL(res);
//     const enosh = document.getElementById('image-enosh')
//     enosh.setAttribute('src', img)
//     enosh.style['display'] = 'block'
// })

const setImage = async (url, imageId) => {
    getImage(url).then((blob) => {
        const src = URL.createObjectURL(blob);
        const img = document.getElementById(imageId)
        img.setAttribute('src', src)
        img.style['display'] = 'block'
    })
}

async function alertos() {
  await setImage("http://localhost:5000/api/questions_a/the_deadliest_attack_types", 'image-tzvi')
}
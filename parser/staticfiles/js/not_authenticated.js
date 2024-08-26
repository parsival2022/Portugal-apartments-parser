
const toggleModal = () => {
    const modal = document.getElementById('wrongKeyModal') || null
    if(!modal) return
    modal.toggle()
}
document.addEventListener('DOMContentLoaded', toggleModal, false)
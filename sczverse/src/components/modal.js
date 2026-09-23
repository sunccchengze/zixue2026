
export function openModal(html){
  const modal=document.getElementById('modal');
  const content=document.getElementById('modal-content');
  content.innerHTML=html;
  modal.classList.remove('hidden');
}
export function closeModal(){ document.getElementById('modal').classList.add('hidden'); }

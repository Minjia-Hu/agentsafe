"use strict";
const tabs = Array.from(document.querySelectorAll('[role="tab"]'));
function selectTab(tab) {
  for (const item of tabs) {
    const selected = item === tab;
    item.setAttribute('aria-selected', String(selected));
    item.tabIndex = selected ? 0 : -1;
    document.getElementById(item.dataset.panel).hidden = !selected;
  }
}
for (const tab of tabs) {
  tab.addEventListener('click', () => selectTab(tab));
  tab.addEventListener('keydown', (event) => {
    let index = tabs.indexOf(tab);
    if (event.key === 'ArrowRight') index = (index + 1) % tabs.length;
    else if (event.key === 'ArrowLeft') index = (index + tabs.length - 1) % tabs.length;
    else if (event.key === 'Home') index = 0;
    else if (event.key === 'End') index = tabs.length - 1;
    else return;
    event.preventDefault(); selectTab(tabs[index]); tabs[index].focus();
  });
}
function bindReviewCards(root = document) {
for (const card of root.querySelectorAll('.file-card')) {
  const toggle = card.querySelector('.overlay-control');
  if (toggle) toggle.addEventListener('change', () => card.classList.toggle('regions-hidden', !toggle.checked));
  for (const button of card.querySelectorAll('button[data-target]')) {
    button.addEventListener('click', () => {
      for (const row of card.querySelectorAll('button[data-target]')) row.setAttribute('aria-pressed', String(row === button));
      for (const target of card.querySelectorAll('.region, .log-line')) target.classList.toggle('active', target.id === button.dataset.target);
      if (button.classList.contains('log-finding')) {
        const line = Array.from(card.querySelectorAll('.log-line')).find(item => item.id === button.dataset.target);
        if (line) {
          line.focus({preventScroll: true});
          line.scrollIntoView({block: 'nearest', inline: 'nearest'});
        }
      } else {
        card.classList.remove('regions-hidden');
        if (toggle) toggle.checked = true;
      }
    });
  }
}
}
bindReviewCards();

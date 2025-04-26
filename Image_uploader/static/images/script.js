const page = parseInt(new URLSearchParams(window.location.search).get('page')) || 1;
if (page < 1) {
    window.location.href = '/images/?page=1';
}


fetch('/api/images_count/').then(response => response.json()).then(count => {
    let imagesCount = count.count;
    let pagesCount = Math.ceil(count.count / 10);
    if (page > pagesCount) {
        window.location.href = '/images/?page=' + pagesCount;
    }
    const prevPage = addPaginationButton(page - 1, '⟵', false, pagesCount);
    for (let i = 1; i <= pagesCount; i++) {
        addPaginationButton(i, '', i == page);
    }
    const nextPage = addPaginationButton(page + 1, '⟶', false, pagesCount);
});


const tbody = document.getElementById('imagesTableBody');
fetch('/api/images/', { headers: {'Page': page } })
.then(response => response.json())
.then(images => setImages(images.images));

function setImages(images) {
    const imagesContainer = document.createElement('div');
    images.forEach(image => {
        const fullname = image.filename + image.file_type;

        const tr = document.createElement('tr');

        const tdPreview = document.createElement('td');
        const tdName = document.createElement('td');
        const tdOrigName = document.createElement('td');
        const tdSize = document.createElement('td');
        const tdDate = document.createElement('td');
        const tdType = document.createElement('td');
        const tdDelete = document.createElement('td');


        const deleteButton = document.createElement('button');
        deleteButton.onclick = () => {
            fetch(`/api/delete/${fullname}`, {method: 'DELETE'})
            .then(data => {
                location.reload();
            });
        }
        deleteButton.innerHTML = '<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg" viewBox="0 0 16 16"> <path d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8z"/></svg>';
        deleteButton.classList.add('delete-btn');
        tdDelete.appendChild(deleteButton);

        tdPreview.innerHTML = `<img src="/images/${fullname}" width="42" height="100%">`;

        tdOrigName.innerHTML = image.original_name;

        tdSize.innerHTML = Math.round(image.size / 1024, 2) + ' KB';

        tdDate.innerHTML = image.upload_time;

        tdType.innerHTML = image.file_type;

        tdName.innerHTML = `<a href="/images/${fullname}" target="_blank">${image.filename}</a>`;

        tr.appendChild(tdPreview);
        tr.appendChild(tdName);
        tr.appendChild(tdOrigName);
        tr.appendChild(tdSize);
        tr.appendChild(tdDate);
        tr.appendChild(tdType);
        tr.appendChild(tdDelete);

        tbody.appendChild(tr);
    });
    document.body.appendChild(imagesContainer);
}

function addPaginationButton(page, text, active, pagesCount) {
    if (text == '') {
        text = page;
    }
    const li = document.createElement('li');
    if (page < 1 || page > pagesCount) {
        li.classList.add('disabled');
    }
    li.classList.add('page-item');
    if (active) {
        li.classList.add('active');
    }
    const a = document.createElement('a');
    a.classList.add('page-link');
    a.href = `/images/?page=${page}`;
    a.innerHTML = text;
    li.appendChild(a);
    console.log(li);
    document.getElementById('pagination').appendChild(li);
    return li;
}

document.getElementById('btnGoToUpload').addEventListener('click', (event) => {
    window.location.href = '/upload/';
});


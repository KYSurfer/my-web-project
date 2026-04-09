<template>
    <footer class="footer">
        <div class="footer__main">
            <div>
                <div class="footer__main-logo">
                    <img src="../assets/images/bons-burgers-logo-removebg.png" alt="Bon's Burgers лого" class="footer__main-logo-img">
                    <div class="footer__main-logo-text">
                        <h2 class="footer__main-logo-text-name">Bon's Burgers</h2>
                        <span class="footer__main-logo-text-est">est. 1974</span>
                    </div>
                </div>
                <div class="footer__main-under-logo">
                    <span>Вместе навсегда!</span>
                    <span>BUNNY SMILES INC. © 1974</span>
                </div>
            </div>
            <div class="footer__main-contacts">
                <h2>Контакты</h2>
                <span>Брайтон, Висконсин</span>
                <span>(555) 294-2453</span>
                <span>info@bonsburgers.com</span>
            </div>
        </div>
        <div class="footer__bottom">
            <div class="footer__bottom-txt">© 1974 Bon's Burgers / Bunny Smiles Inc. All Rights Reserved.</div>
            <div>Создаем улыбки с 1974</div>
        </div>
    </footer>
</template>

<script></script>

<style scoped>
    .footer{
        background-color: black;
        border-top: 3px solid var(--vintage-yellow);
        overflow: hidden;
    }

    .footer__main{
        margin-top: 50px;
        margin-bottom: 40px;
        display: flex;
        justify-content: center;
        gap: 150px;
    }
    
    .footer__main-logo{
        display: flex;
        align-items: center;
    }

    .footer__main-logo-img{
        width: 50px;
        object-fit: cover;
    }

    .footer__main-logo-text{
        display: flex;
        font-family: 'Dessau-', sans-serif;
        color: gray;
        flex-direction: column;
    }
    
    .footer__main-logo-text-name{
        font-family: 'Dessau-Heavy', sans-serif;
        text-shadow: -2px 2px var(--blood-red);
        color: var(--vintage-yellow);
    }

    .footer__main-logo-text-est{
        font-family: 'EkiR';
        margin-top: -5px;
        font-size: 8px;
    }

    .footer__main-under-logo{
        display: flex;
        flex-direction: column;
        font-family: 'EkiR';
        color: gray;
        gap: 10px;
        font-size: 8px;
        margin-block: 20px;
    }

    .footer__main-contacts{
        display: flex;
        flex-direction: column;
        gap: 15px;
        font-family: 'Uncage';
        color: var(--text-light);
    }

    .footer__bottom{
        display: flex;
        justify-content: center;
        flex-direction: column;
        align-items: center;
        padding-bottom: 30px;
        font-family: 'EkiR', sans-serif;
        font-size: 8px;
        color: var(--text-light);
        gap: 5px;
    }

    .footer__bottom-txt {
    padding-inline: 100px;
    border-top: 1px solid var(--vintage-yellow);
    width: fit-content;
    padding-top: 20px;
    
}
</style>
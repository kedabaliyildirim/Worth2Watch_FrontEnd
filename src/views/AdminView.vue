<template>
  <div class="mainAdmin">
    <form v-if="!loginState" class="loginForm" @submit.prevent="login">
      <!-- <input type="hidden" name="_token" :value="csrf"> -->
      <label for="email">Email:</label>
      <input type="email" id="email" v-model="email" required />
      <label for="password">Password:</label>
      <input type="password" id="password" v-model="password" required />
      <button type="submit" login>Login</button>
    </form>
    <div v-if="loginState">
    Lorem ipsum dolor sit amet consectetur, adipisicing elit. Nesciunt, esse unde reiciendis magni soluta beatae obcaecati saepe eum? Obcaecati minima aut illo accusamus ad quod sed culpa explicabo voluptatem dignissimos?
    Doloremque perferendis magnam odio nam sunt consectetur maiores voluptates ut unde magni inventore impedit accusamus quasi, delectus nihil architecto voluptatibus similique facilis consequuntur porro quis officia! Quasi corrupti consequuntur tenetur.
    Porro sit rerum veritatis tenetur facere, natus rem laudantium voluptate eos ad, itaque adipisci hic magni omnis tempora pariatur! Repudiandae beatae incidunt facere aliquid perferendis fuga veritatis in tenetur inventore!
    Modi assumenda cumque, delectus eius unde dolor eveniet sequi enim laborum, maiores ea adipisci suscipit nobis ratione consequuntur dicta doloremque. Repudiandae quasi quod soluta recusandae temporibus commodi, repellat esse illo?
    Ullam quisquam quidem minus ut provident, nam harum. Omnis minus odit quo sint? Dolor laboriosam totam et deserunt maiores quae aperiam dolorem. Vitae corporis quaerat iusto excepturi, ea accusamus architecto!
    Quidem eum eos saepe velit natus itaque magni, perferendis ipsa error quae earum quaerat dolorum eaque ea accusantium molestiae tempore reiciendis debitis expedita, pariatur possimus asperiores tempora modi nobis! In.
    Quam consequuntur porro sit consequatur saepe, itaque incidunt. Eius pariatur hic incidunt minus ea. Odit cum vero porro provident nemo fuga excepturi! Consequatur omnis, mollitia sed illum soluta necessitatibus dolorum.
    Praesentium aspernatur natus dolore sit esse! Similique rerum exercitationem vero provident necessitatibus nobis, explicabo, corporis facilis unde vitae eius? Iste accusantium, quia quis officiis nesciunt maxime qui architecto fugit. Dolorum?
    Dolorem impedit voluptate qui laudantium harum tempora provident voluptas fugiat ab deleniti cum perspiciatis maxime dolor voluptatibus beatae suscipit quaerat vero necessitatibus debitis eius, perferendis iste optio. Atque, impedit accusantium?
    Voluptate minima fuga ab aspernatur at culpa eveniet ex magni, a libero impedit in esse illum neque nostrum dicta minus amet reiciendis enim quibusdam mollitia placeat? Doloremque id amet velit?
    Omnis aut qui accusantium, necessitatibus tempore voluptate ducimus culpa, est soluta voluptatum architecto quisquam aliquam ipsam libero assumenda magnam commodi illo quibusdam. Deserunt ipsa est minus pariatur consequatur. Libero, eius?
    Error minus eius fugit explicabo iste, unde molestias natus. Soluta quaerat facilis ad maxime quia tempora aliquam vel esse accusantium consequatur. Voluptatibus totam necessitatibus cupiditate reprehenderit. Vel dolor non consequuntur.
    Expedita pariatur obcaecati repudiandae architecto tempora voluptatem ducimus quisquam quae perferendis porro sed sint nisi aut iure velit totam, magni magnam explicabo nulla voluptate placeat beatae impedit eveniet. Cumque, ut.
    Voluptate, iste ullam! Repudiandae harum, iusto facere quasi, expedita eligendi aut sunt rem consequatur voluptates nobis dicta maiores ratione? Quasi eligendi veritatis illo alias beatae adipisci aut corporis culpa explicabo!
    Facere, quas ut perspiciatis eaque eius dignissimos reiciendis deleniti enim in sint, laborum libero. Nihil sequi, necessitatibus voluptatum voluptate in dolor perspiciatis vero qui porro maiores reprehenderit vel omnis et?
    Dicta excepturi quod, eum voluptas veritatis delectus sapiente dolorum, minus maiores ab aspernatur sit non voluptates blanditiis consequuntur inventore molestiae reiciendis repellat tempore obcaecati! Asperiores facere vero reprehenderit harum dolor.
    Tenetur a quo laudantium, illum ea quidem perferendis omnis aut neque quam voluptates repellat natus! A velit nihil eius tempore architecto ipsam temporibus aliquam nulla, atque earum minus assumenda. Enim.
    Aspernatur, iusto. Eum accusamus tempora nihil molestias nisi totam minima blanditiis voluptas dicta quas, velit temporibus eveniet repellendus. Vel similique quod tempora quis quas fugiat maxime modi sed repudiandae delectus.
    Atque assumenda dolor, recusandae aspernatur at praesentium reprehenderit. Placeat quis possimus aliquam voluptate nulla aut quidem at, laborum aspernatur inventore distinctio suscipit saepe in alias doloremque necessitatibus perspiciatis? Aspernatur, sint!
    Deleniti porro accusantium reiciendis nobis placeat fugit, at suscipit laborum autem quibusdam debitis amet totam maxime ex aliquid rem qui libero nihil nulla accusamus consectetur dolorem. Sapiente nulla similique itaque.
    Hic unde eum facilis maiores. Aliquam et doloremque itaque voluptatibus cupiditate perferendis velit numquam consequatur accusamus quibusdam? Quae aliquid illo voluptatibus fuga voluptate excepturi molestiae est nam libero? Fugiat, illo!
    Ab, voluptates tempora iure corrupti accusamus numquam dolorum fuga esse illum quae, repellat libero repellendus quidem praesentium quia doloremque nostrum sint sed animi, quaerat fugit delectus. Iusto quibusdam quae voluptate.
    Non suscipit ipsum esse, id vitae quae illo ad corporis dolores voluptatum, voluptatibus quasi tempore nobis necessitatibus aut quaerat temporibus eveniet odio a minima impedit, nemo ut mollitia. Ad, id?
    Asperiores ex eveniet dolorem blanditiis, tempora voluptates quam accusamus totam modi, culpa assumenda placeat ratione amet molestias, illum ut repellat saepe id sint. Facere odio repudiandae pariatur aliquam enim sunt.
    Aperiam eius similique magnam ratione consequuntur veniam tenetur est neque eaque omnis doloremque facilis quos voluptate accusantium possimus nam harum minima, commodi optio, facere eveniet distinctio officiis. Reprehenderit, amet dicta!
    Maxime veniam natus maiores ipsa ab eligendi sunt culpa ducimus esse, molestias saepe officia laudantium facilis repudiandae explicabo modi asperiores. Ratione ullam laborum esse ea vitae corporis in, molestias facilis?
    In temporibus dolores enim repellat distinctio excepturi nam pariatur quae voluptatem, totam voluptate nesciunt eaque, quibusdam voluptatum quo voluptas fuga veniam cum? Molestias veritatis aperiam vitae voluptate accusantium voluptates expedita?
    Voluptatem tenetur ipsum voluptatum, molestias cupiditate ratione similique. Optio repellat enim tempore, repellendus fugit consequuntur voluptatum hic, illum quas magnam perspiciatis exercitationem veniam iusto quia, similique quae. Soluta, libero et?
    A labore facere autem placeat tenetur ullam dolores soluta repellendus, laudantium id temporibus, pariatur in corporis asperiores dolorum sint recusandae ratione provident assumenda esse eligendi? Praesentium ea impedit explicabo enim?
    Similique quas quasi excepturi, expedita qui tempore quibusdam laborum repudiandae delectus rem totam ipsam et consequuntur! Repellat, eos natus minima, repellendus ipsam, magnam nisi at commodi ullam iusto qui labore.
    Asperiores sit autem quas totam maxime cum id ullam? Nam perspiciatis natus doloribus sed nesciunt necessitatibus sit porro assumenda, totam tempore! Sequi, impedit blanditiis eveniet doloribus dolorum repellat ducimus maxime.
    Labore, consequatur. Reiciendis, cupiditate! Error deserunt in, fugit vel ex eius dolor sapiente culpa possimus sunt consequuntur voluptas incidunt ab commodi, iure eligendi. Ut magnam pariatur reprehenderit numquam sapiente nam.
    Impedit neque cumque obcaecati quo commodi quam cum aspernatur saepe id aperiam a incidunt fugiat illum eaque perferendis nesciunt suscipit provident voluptatum esse numquam iusto, atque rem unde. Quis, aperiam.
    Ullam earum eos distinctio! Fuga repellendus, quae dolores vitae hic deleniti rerum unde minus at accusantium vel dolor culpa nobis obcaecati illo facilis nihil necessitatibus? Consectetur ducimus minima fugit expedita!
    Odio illum reprehenderit, saepe quia nisi eos ipsa, cumque possimus omnis voluptatem, in amet nemo? Temporibus beatae sit laudantium eligendi commodi aut nemo, quas labore repellendus aliquam sed, natus excepturi.
    Pariatur neque, quam facilis ea expedita, nihil voluptate vero tempora nam magni dolor ipsam hic omnis modi porro recusandae ratione. Totam saepe nostrum molestiae officiis! Expedita itaque laudantium voluptatum ipsam.
    Perferendis aperiam a, alias beatae dicta reprehenderit aut. Veniam modi saepe consectetur pariatur earum possimus aspernatur recusandae dolore corrupti soluta molestias, quas officia voluptatibus sapiente aliquid dolor necessitatibus voluptatem quae?
    Ullam ad voluptatibus tenetur molestias architecto veniam est quisquam totam quo, praesentium consequatur eaque facere adipisci atque, ut sapiente recusandae rerum tempore ea veritatis ipsa? Accusantium laborum explicabo voluptates quis.
    Ea reiciendis facere quasi recusandae. Numquam tempore maxime harum dolores voluptatibus quisquam dicta iste magni alias voluptates earum, reiciendis aut laudantium quas nulla corrupti commodi impedit expedita quod pariatur quam!
    Cumque odio quibusdam quae sint omnis perspiciatis eos doloribus autem quasi voluptatum cum deleniti nisi neque quo, voluptate labore facere iste vitae excepturi odit, itaque repellat consequuntur in! Corporis, expedita?
    Neque natus quibusdam sunt voluptates non hic tempora aliquid id quaerat, deleniti quia voluptas consectetur qui architecto iusto? Facilis, eos quaerat delectus placeat ut inventore iusto quod nisi minima exercitationem?
    Quod illum alias repellat consequatur tempore nam odio corrupti! Quae fugit nesciunt dolore. Officiis velit incidunt ipsam quos voluptatem aliquid tempora cupiditate repellat quisquam recusandae, aliquam sint sequi architecto commodi?
    Nihil ducimus tempora, est ad quasi aspernatur? Repellendus, veniam architecto, excepturi fugit sed odio id aliquam incidunt deserunt commodi esse voluptatum praesentium a. Magni assumenda quo vel quibusdam, molestiae ipsum!
    Perferendis pariatur numquam atque architecto qui rem, ullam quae eius dolor nemo fuga quos magnam quis, aspernatur labore sed ex hic. Mollitia expedita nisi deleniti molestiae animi, laudantium nostrum sequi!
    Aliquid natus iure mollitia facere, repellendus odit inventore incidunt placeat, ducimus id, culpa voluptatem amet. Nisi corrupti officia voluptatem, harum reprehenderit, doloremque fuga quo necessitatibus amet perferendis sunt odit animi!
    Voluptatem velit ratione, culpa ab officiis quis odio atque excepturi soluta explicabo consequatur nemo rerum, maiores pariatur nam quidem qui vitae aliquam aspernatur optio dolore quos cupiditate. Quam, corporis voluptates.
    Ratione consequatur magnam deleniti quos qui voluptas libero earum quas veniam. Magni, explicabo quia minus illum mollitia architecto, iusto distinctio iure quas placeat tenetur hic quo earum impedit eligendi veniam.
    Consectetur nesciunt sint molestias sit praesentium necessitatibus magnam? Adipisci, veniam laudantium provident deserunt dolore quaerat fuga ullam ipsa possimus, eligendi tempora ea ratione eum magni explicabo odio reiciendis repudiandae ab?
    Tenetur debitis tempora repellat similique, officiis ea sed necessitatibus asperiores dicta neque cum sapiente quas earum molestiae? Numquam explicabo, nisi quasi reprehenderit, dolores recusandae ex voluptatum, nihil dolorum blanditiis qui.
    Quae aut earum ut cum eaque. Repellat veniam accusamus, officia natus numquam, necessitatibus repellendus ipsum nam, maiores sequi amet consectetur praesentium omnis in ducimus facilis quibusdam. Modi dolores beatae repudiandae!
    Rem corporis aut quos neque est maiores, ducimus totam possimus. Neque velit iure iste rerum placeat at consequuntur est, sit a provident suscipit error similique nisi fugit, ipsum doloribus sint?
    Ipsa veniam delectus excepturi dolorum obcaecati praesentium debitis, id ullam. Harum saepe sequi pariatur autem exercitationem temporibus magnam, fuga fugiat itaque est, impedit consequatur nulla expedita ad quos voluptatem esse.
    Iste provident optio adipisci cum! Iste, natus. Obcaecati esse molestiae nihil velit et iusto commodi, dolorum dolore pariatur omnis? Quos enim asperiores nulla cupiditate necessitatibus. Nesciunt at perferendis laboriosam minima.
    In impedit non minus hic quisquam illo accusamus rem, dolore dignissimos, enim accusantium odit molestias! Sit nam numquam ipsa tempora sapiente, dolorem vero delectus, aut aperiam eveniet perferendis praesentium non.
    Facere natus autem veniam quisquam esse aliquid quidem eaque, ipsam distinctio labore id dignissimos accusantium quaerat impedit fuga. Debitis cumque voluptatem similique qui inventore. Repellendus modi minus qui sequi nobis!
    Architecto et inventore itaque eius dolorem placeat sit similique sed velit molestias maiores non fuga provident mollitia, cupiditate adipisci recusandae? Beatae explicabo repellat, cumque assumenda dicta nam magni ad nisi.
    Accusantium beatae nesciunt alias doloribus, ad reiciendis earum perspiciatis, necessitatibus accusamus fugit, quaerat facilis? Saepe aperiam quisquam, ut maiores aliquam recusandae. Vitae quod illum aperiam, numquam consectetur iure sed saepe.
    Dolore, tenetur doloribus quas optio nam ad adipisci harum fugiat facilis, odit ipsam? Neque excepturi ut tenetur totam, aliquam ex, deserunt esse nostrum error natus, eum id unde vero inventore.
    Aliquam eligendi minus temporibus numquam nemo magni unde, tenetur natus aperiam vel fuga accusamus doloribus, enim consectetur quae placeat praesentium et ipsam quam commodi iure dicta quos dolorum! Maiores, error?
    Ab quas iste cum laboriosam qui aut necessitatibus fugiat rem nobis. Natus aspernatur expedita eius, amet culpa laudantium, itaque ut nam voluptates perferendis iusto veritatis magni vero libero consequuntur. Rerum.
    Animi iusto est repellendus delectus. Explicabo, cum obcaecati consequatur quae laboriosam cumque reiciendis aliquam culpa ducimus aut tempore, quisquam fugit rem accusamus voluptas delectus officiis. Repellat nihil ab amet ea.
    Autem expedita beatae maxime odit, vero quisquam asperiores unde velit fugiat assumenda harum suscipit? Earum quae nam molestias iusto. Ipsum, eos quisquam suscipit aspernatur perferendis cupiditate assumenda fugit officiis amet.
    Recusandae deleniti, incidunt consequuntur, omnis in illo deserunt vitae vero nemo eveniet ipsa. Aliquid, fugit optio sit quo eveniet in vero ea incidunt, hic culpa laborum inventore. Assumenda, doloremque eos.
    Quaerat, consequatur non, facere dolor totam iusto at velit aliquam praesentium soluta, similique accusantium consequuntur? Architecto, unde! Voluptates eaque beatae quae iusto quisquam. Fugit placeat similique, necessitatibus exercitationem suscipit non.
    Cum ab quam nostrum enim aliquam deserunt sed, corrupti, fugit dolorum asperiores, dicta pariatur cupiditate explicabo. Cum tempore tenetur impedit ad soluta debitis fuga saepe? Animi vero neque architecto labore.
    Libero minus asperiores sit. Dolor animi quod sit cupiditate similique consequatur deserunt a fugit soluta neque, eos ex sed nisi iusto? Amet, beatae eveniet. Distinctio id voluptatum amet quae omnis?
    Ad neque aperiam iusto itaque a dolores excepturi temporibus sequi voluptate rerum, voluptatibus sed ducimus eligendi explicabo est perferendis aspernatur facere! Fugit praesentium rerum maxime, quia dignissimos architecto earum obcaecati!
    Ducimus sequi porro, enim culpa, amet blanditiis necessitatibus quos ab perferendis dolore dignissimos. Temporibus sunt aliquid atque accusantium nam quam quo facilis magnam at qui, mollitia eaque, soluta veniam sapiente?
    Libero nemo soluta ab ratione assumenda aliquid eius rem quam inventore nihil labore aspernatur veritatis nostrum expedita quo sequi, pariatur eaque vel ducimus dicta! Accusamus beatae itaque tempora eveniet ipsum.
    Numquam esse ipsum tempora incidunt odit assumenda veniam illum, unde eaque? Dicta voluptas impedit nesciunt deserunt explicabo molestiae magni dolores velit atque beatae! Temporibus libero incidunt officia consectetur et inventore?
    Sit deserunt fuga ad quae corporis eaque accusamus et voluptates consequuntur? Enim velit recusandae cupiditate debitis, aspernatur laudantium inventore, non nostrum sunt quos minus dolorem consequatur iusto voluptatem vero neque.
    Exercitationem, temporibus earum! Adipisci aperiam, voluptates optio ea nobis doloribus iure ab asperiores excepturi quae nihil, assumenda neque beatae laudantium aliquam sequi non sapiente modi dolor. Incidunt fuga cumque soluta!
    Rerum tempore atque harum blanditiis quas. Tenetur consectetur corporis unde adipisci numquam obcaecati quos recusandae provident, fuga hic nisi praesentium delectus eligendi odio aliquid? Maiores perspiciatis nemo suscipit repellat eveniet!
    Harum voluptatibus officiis repellat ea ex animi impedit deleniti voluptatum earum provident temporibus dignissimos necessitatibus, quasi dolorum sint ipsa voluptate reprehenderit corporis ut soluta veritatis, porro maxime blanditiis doloribus! Molestias.
    Iure animi molestiae voluptatem culpa cumque esse quaerat laudantium veritatis iste ullam magnam ea sit accusantium, quo voluptate at. Alias animi assumenda harum. Ab dolorem quisquam quod suscipit dicta natus.
    Vitae perferendis, quisquam tempora ducimus neque nobis tempore ut atque mollitia fugiat quos officia expedita alias laudantium porro odio eaque dolor! Impedit assumenda natus doloremque corporis eveniet excepturi quasi pariatur!
    Modi sequi voluptas corporis sapiente adipisci in magni hic at dolores! Doloremque soluta esse beatae laboriosam laudantium quam tenetur unde obcaecati dolorem placeat, eum eius debitis natus minus ut expedita.
    At quos aperiam molestiae? Quidem explicabo non natus quam nam sequi, perspiciatis consectetur repellat ex itaque odio! Tempore voluptate aspernatur obcaecati maiores neque veniam optio iste est aperiam. Fuga, id.
    Soluta velit sequi consequatur dolorem labore atque suscipit necessitatibus reiciendis optio accusantium exercitationem iste, laudantium vel? Quia eos dicta aliquid suscipit voluptate quae ipsa non deleniti ea nobis? Nemo, pariatur.
    Nam qui error temporibus dolorum eos facere aliquid delectus magnam! Eum nam numquam ratione maiores, laudantium ipsa, quia laborum assumenda recusandae neque enim. Voluptate ex facilis incidunt voluptatum sequi porro!
    Tempora aut voluptate perferendis doloremque, provident nemo adipisci unde optio sed id consequatur corporis consectetur architecto dignissimos possimus sequi omnis, quam repellendus! Eos quibusdam nesciunt, debitis in velit tempora itaque.
    Neque blanditiis quod amet, beatae aspernatur tempora accusamus consequuntur animi dignissimos error porro ducimus. Aperiam, officia placeat, mollitia dolore maiores laborum sapiente assumenda at rerum maxime saepe? Laudantium, sunt aliquid.
    Tempore distinctio veritatis assumenda explicabo deserunt minus, quod autem itaque error, necessitatibus unde qui culpa, sequi libero ducimus ab quisquam neque quos. Nam repellat hic accusamus reprehenderit odio distinctio omnis!
    Maxime dolorem aspernatur, in debitis nam ex vitae perferendis? Tempore corrupti illum saepe ipsam, error delectus quo optio aliquid voluptates vel sit quidem iste harum non quaerat expedita distinctio repudiandae?
    Tempora dolorum commodi quas, libero repellat blanditiis? Inventore cupiditate rem asperiores, fugit cum magni incidunt accusamus, eaque expedita quasi a eum necessitatibus repellat quos molestias optio magnam vitae error similique!
    Quaerat, exercitationem? Deserunt dolorem modi, qui nulla minus fugiat illo voluptatem sed dolores, possimus iusto sequi eos ut repudiandae a ducimus ex repellat consequuntur voluptas ea enim tempore placeat assumenda.
    A possimus rerum, fugiat tenetur corporis maxime ullam in quae placeat ipsa ducimus commodi perspiciatis voluptates iste. Repellendus minus libero, dolorum modi temporibus reprehenderit tenetur quos non harum sunt dolorem?
    Voluptatem, dolorem. Quidem dolorum eaque id totam, dignissimos veritatis consectetur iure, nesciunt quas recusandae voluptatem illum ducimus culpa quisquam maxime cumque aperiam voluptatibus eum eius, eos quae odio impedit eligendi?
    Maxime neque dolor dicta hic, voluptate consequuntur ea aliquam dignissimos, delectus, corporis dolores laboriosam sed iste earum nulla eius recusandae harum? Delectus quia ipsum harum voluptas blanditiis deserunt illo sunt?
    Illo dignissimos vero hic harum porro, ea nisi quaerat. Consequatur cupiditate omnis, esse autem doloribus, eius pariatur obcaecati iste ratione ad tempore optio iure aliquam, laborum porro velit recusandae excepturi!
    Impedit vitae unde ea nisi quos, labore quod officiis aperiam temporibus, voluptates sapiente eaque eos doloribus suscipit? Mollitia molestias quasi, repellendus, numquam repudiandae modi ipsum voluptates nobis ipsam, deleniti distinctio.
    Tempore temporibus saepe error ad, dolorum culpa illo eum eaque commodi, facere perferendis est assumenda ex deserunt labore nobis? Inventore beatae repudiandae voluptatem, eius exercitationem temporibus iure quibusdam ipsum unde?
    Voluptas, voluptates doloribus ex esse aperiam quidem eaque, exercitationem maxime quisquam nam provident magni consectetur corrupti soluta nesciunt architecto blanditiis quibusdam, modi deserunt dignissimos inventore! Impedit inventore eaque sunt similique.
    Voluptatibus expedita culpa cupiditate ad, ea dolorem nihil molestias? Rem, soluta corrupti! Autem itaque quod, doloremque quas eum atque voluptatem, earum tempora delectus consequatur illum fuga facilis ipsam quos voluptatibus.
    Itaque accusamus quo illo sed at consequuntur tempore ducimus nemo alias, autem perferendis, quas consectetur sapiente quibusdam voluptatum molestiae! Aliquam numquam perspiciatis sequi voluptate minima mollitia blanditiis itaque voluptatibus animi.
    Dolores veritatis ab corrupti error hic fugiat enim expedita? Consectetur, fugit. Qui, itaque dignissimos corporis voluptates dolore molestias voluptate exercitationem dolorem minima nesciunt, porro saepe repellendus modi officiis, quisquam non.
    Sunt ad accusantium eaque mollitia inventore repellat impedit dicta obcaecati quisquam iure quae sit, velit, eius corrupti quod sed excepturi dolorem incidunt neque nemo? Necessitatibus maxime iste provident hic omnis.
    Saepe, laudantium et nulla incidunt eum iusto alias. Magni minus eveniet quasi nihil, velit tempore ut culpa maxime eum, temporibus nulla. Unde quas consequuntur voluptatibus repudiandae possimus inventore, dolorem cupiditate!
    Tenetur pariatur aliquid inventore magni voluptatum facere possimus amet corporis at repudiandae! Aspernatur quibusdam nemo ipsum. Natus ad incidunt soluta voluptatum adipisci voluptates aliquam repellat, unde commodi a ipsum. Harum.
    Aliquam nostrum accusantium dicta totam repellat eos, et quisquam molestias quasi vero illo delectus quod numquam eius officia iusto velit reprehenderit cum dolore voluptatibus eveniet, exercitationem temporibus eligendi! Consequatur, aliquid!</div>
  </div>
</template>

<script>
export default {
  name: 'AdminView',
  data() {
    return {
      email: '',
      password: '',
    }
  },
  methods: {
    async login() {
      const payload = {
        email: this.email,
        password: this.password
      }
      this.$store.dispatch('login', payload)
    }
  },
  computed: {
    loginState() {
      return this.$store.getters.getLoginState
    },
    csrfState() {
      this.$store.getters.getCsrftoken
      return this.$store.getters.getCsrftoken
    }
  }
}
</script>

<style>
.loginForm {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}
button {
  margin: 15px;
  border-radius: 5%;
}
</style>

## 爬取全部CVPR论文列表

todo

---

- [ ] 从[CVPR 2025 Open Access Repository](https://openaccess.thecvf.com/CVPR2025?day=all)爬取所有CVPR论文

- [ ] 输出内容如下：

bib:

```bibtex
@InProceedings{Xiao_2025_CVPR,
    author    = {Xiao, Bohan and Wang, Peiyong and He, Qisheng and Dong, Ming},
    title     = {Deterministic Image-to-Image Translation via Denoising Brownian Bridge Models with Dual Approximators},
    booktitle = {Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)},
    month     = {June},
    year      = {2025},
    pages     = {28232-28241},
   url={https://openaccess.thecvf.com/content/CVPR2025/html/Xiao_Deterministic_Image-to-Image_Translation_via_Denoising_Brownian_Bridge_Models_with_Dual_CVPR_2025_paper.html}
}


@InProceedings{Ahmed_2025_CVPR,
    author    = {Ahmed, Sk Miraj and Basaran, Umit Yigit and Raychaudhuri, Dripta S. and Dutta, Arindam and Kundu, Rohit and Niloy, Fahim Faisal and Guler, Basak and Roy-Chowdhury, Amit K.},
    title     = {Towards Source-Free Machine Unlearning},
    booktitle = {Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)},
    month     = {June},
    year      = {2025},
    pages     = {4948-4957},
   url={https://openaccess.thecvf.com/content/CVPR2025/html/Ahmed_Towards_Source-Free_Machine_Unlearning_CVPR_2025_paper.html}
}
```

ris:

```ris
TY  - CONF
AU  - Xiao, Bohan
AU  - Wang, Peiyong
AU  - He, Qisheng
AU  - Dong, Ming
TI  - Deterministic Image-to-Image Translation via Denoising Brownian Bridge Models with Dual Approximators
T2  - Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)
PY  - 2025
DA  - 2025/06/01
SP  - 28232-28241
UR  - https://openaccess.thecvf.com/content/CVPR2025/html/Xiao_Deterministic_Image-to-Image_Translation_via_Denoising_Brownian_Bridge_Models_with_Dual_CVPR_2025_paper.html
ER  - 

TY  - CONF
AU  - Ahmed, Sk Miraj
AU  - Basaran, Umit Yigit
AU  - Raychaudhuri, Dripta S.
AU  - Dutta, Arindam
AU  - Kundu, Rohit
AU  - Niloy, Fahim Faisal
AU  - Guler, Basak
AU  - Roy-Chowdhury, Amit K.
TI  - Towards Source-Free Machine Unlearning
T2  - Proceedings of the Computer Vision and Pattern Recognition Conference (CVPR)
PY  - 2025
DA  - 2025/06/01
SP  - 4948-4957
UR  - https://openaccess.thecvf.com/content/CVPR2025/html/Ahmed_Towards_Source-Free_Machine_Unlearning_CVPR_2025_paper.html
ER  - 
```



### 方法一

- idea：保存网页内容到html，从html中解析所有论文的bibtex
- run：
  1. 为防止页面没有全部加载，手动用鼠标将页面拖到底部，再另存网页为`CVPR 2025 Open Access Repository.html`
  2. run `get-bib-url-from-html.py`, 
  3. 生成: `cvpr-papers.bib`, ` cvpr-papers.ris`

### 方法二（推荐）

- idea: 直接使用python模拟浏览器操作，获取url中的内容，并解析论文信息

- run：
  1. run ` get-bib-url-from-url.py`
  
  2. 生成: `cvpr-papers.bib`, ` cvpr-papers.ris`
  
     



## convert bib to ris

- convert2risViare.py

  